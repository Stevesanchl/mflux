from typing import TYPE_CHECKING

import mlx.nn as nn
from mlx.utils import tree_flatten

from mflux.models.common.resolution.quantization_resolution import QuantizationResolution
from mflux.models.common.weights.loading.loaded_weights import LoadedWeights
from mflux.models.common.weights.loading.weight_definition import ComponentDefinition

if TYPE_CHECKING:
    from mflux.models.common.weights.loading.weight_definition import WeightDefinitionType


class WeightApplier:
    @staticmethod
    def apply_and_quantize_single(
        weights: LoadedWeights,
        model: nn.Module,
        component: ComponentDefinition,
        quantize_arg: int | None,
        quantization_predicate=None,
    ) -> int | None:
        stored_q = weights.meta_data.quantization_level
        component_weights = weights.components.get(component.name)

        if component_weights is None:
            raise ValueError(f"No weights found for component: {component.name}")

        if quantization_predicate is None:

            def quantization_predicate(path, module):
                return hasattr(module, "to_quantized")

        bits, warning = QuantizationResolution.resolve(stored=stored_q, requested=quantize_arg)

        if warning:
            print(f"⚠️  {warning}")

        if bits is None:
            WeightApplier._validate_native_component(weights, component.name, model, component_weights)
            model.update(component_weights, strict=False)
        elif stored_q is None:
            model.update(component_weights, strict=False)
            if not component.skip_quantization:
                nn.quantize(model, class_predicate=quantization_predicate, bits=bits)
        else:
            if not component.skip_quantization:
                nn.quantize(model, class_predicate=quantization_predicate, bits=bits)
            WeightApplier._validate_native_component(weights, component.name, model, component_weights)
            model.update(component_weights, strict=False)

        return bits

    @staticmethod
    def apply_and_quantize(
        weights: LoadedWeights,
        models: dict[str, nn.Module],
        quantize_arg: int | None,
        weight_definition: "WeightDefinitionType",
    ) -> int | None:
        stored_q = weights.meta_data.quantization_level
        components = {c.name: c for c in weight_definition.get_components()}

        bits, warning = QuantizationResolution.resolve(stored=stored_q, requested=quantize_arg)

        if warning:
            print(f"⚠️  {warning}")

        if bits is None:
            WeightApplier._set_weights(weights, models, components)
        elif stored_q is None:
            WeightApplier._set_weights(weights, models, components)
            WeightApplier._quantize(models, bits, components, weight_definition)
        else:
            WeightApplier._quantize(models, bits, components, weight_definition)
            WeightApplier._set_weights(weights, models, components)

        return bits

    @staticmethod
    def _set_weights(
        weights: LoadedWeights,
        models: dict[str, nn.Module],
        components: dict | None = None,
    ) -> None:
        resolved_components: list[tuple[str, nn.Module, dict]] = []
        for name, model in models.items():
            component_weights = weights.components.get(name)
            if component_weights is None:
                if weights.meta_data.mflux_version is not None:
                    raise ValueError(f"Native MFLUX checkpoint is missing component: {name}")
                continue
            if components is not None:
                component = components.get(name)
                if component is not None and component.weight_subkey is not None:
                    component_weights = component_weights.get(component.weight_subkey, component_weights)
            WeightApplier._validate_native_component(weights, name, model, component_weights)
            resolved_components.append((name, model, component_weights))

        # Validate every native component before mutating any model. A truncated
        # or hand-edited MFLUX index must never leave random initialized weights.
        for _, model, component_weights in resolved_components:
            model.update(component_weights, strict=False)

    @staticmethod
    def _validate_native_component(
        weights: LoadedWeights,
        name: str,
        model: nn.Module,
        component_weights: dict,
    ) -> None:
        if weights.meta_data.mflux_version is None:
            return

        source = dict(tree_flatten(component_weights))
        target = dict(tree_flatten(model.parameters()))
        missing = sorted(target.keys() - source.keys())
        unexpected = sorted(source.keys() - target.keys())
        shape_mismatches = sorted(
            key for key in source.keys() & target.keys() if source[key].shape != target[key].shape
        )
        if missing or unexpected or shape_mismatches:
            raise ValueError(
                f"Native MFLUX {name} checkpoint does not match the MLX module: "
                f"missing={missing[:5]}, unexpected={unexpected[:5]}, "
                f"shape_mismatches={shape_mismatches[:5]}"
            )

    @staticmethod
    def _quantize(
        models: dict[str, nn.Module],
        bits: int,
        components: dict,
        weight_definition: "WeightDefinitionType",
    ) -> None:
        for name, model in models.items():
            component = components.get(name)
            if component and component.skip_quantization:
                continue
            nn.quantize(model, class_predicate=weight_definition.quantization_predicate, bits=bits)
