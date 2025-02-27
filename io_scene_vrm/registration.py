"""
Copyright (c) 2018 iCyP
Released under the MIT license
https://opensource.org/licenses/mit-license.php

"""

from typing import Any

import bpy
from bpy.app.handlers import persistent

from .common import gltf2_addon_support, preferences, shader, version
from .editor import (
    extension,
    glsl_drawer,
    make_armature,
    operator,
    panel,
    property_group,
    validation,
)
from .editor.vrm0 import operator as vrm0_operator
from .editor.vrm0 import panel as vrm0_panel
from .editor.vrm0 import property_group as vrm0_property_group
from .exporter import export_scene
from .importer import import_scene
from .locale.translation_dictionary import translation_dictionary

if persistent:  # for fake-bpy-modules

    @persistent  # type: ignore[misc]
    def add_shaders(_dummy: Any) -> None:
        shader.add_shaders()


classes = [
    gltf2_addon_support.WM_OT_vrm_gltf2_addon_disabled_warning,
    property_group.ObjectPropertyGroup,
    property_group.StringPropertyGroup,
    property_group.FloatPropertyGroup,
    property_group.BonePropertyGroup,
    property_group.MeshPropertyGroup,
    vrm0_property_group.Vrm0MaterialValueBindPropertyGroup,
    vrm0_property_group.Vrm0BlendShapeBindPropertyGroup,
    vrm0_property_group.Vrm0BlendShapeGroupPropertyGroup,
    vrm0_property_group.Vrm0BlendShapeMasterPropertyGroup,
    vrm0_property_group.Vrm0MeshAnnotationPropertyGroup,
    vrm0_property_group.Vrm0DegreeMapPropertyGroup,
    vrm0_property_group.Vrm0FirstPersonPropertyGroup,
    vrm0_property_group.Vrm0HumanoidBonePropertyGroup,
    vrm0_property_group.Vrm0HumanoidPropertyGroup,
    vrm0_property_group.Vrm0MetaPropertyGroup,
    vrm0_property_group.Vrm0SecondaryAnimationCollider,
    vrm0_property_group.Vrm0SecondaryAnimationColliderGroupPropertyGroup,
    vrm0_property_group.Vrm0SecondaryAnimationGroupPropertyGroup,
    vrm0_property_group.Vrm0SecondaryAnimationPropertyGroup,
    # vrm0_gizmo_group.Vrm0FirstPersonBoneOffsetGizmoGroup,
    panel.VRM_PT_current_selected_armature,
    panel.VRM_PT_controller,
    panel.VRM_PT_vrm_armature_object_property,
    vrm0_panel.VRM_PT_vrm0_meta_armature_object_property,
    vrm0_panel.VRM_PT_vrm0_meta_ui,
    vrm0_panel.VRM_PT_vrm0_humanoid_armature_object_property,
    vrm0_panel.VRM_PT_vrm0_humanoid_ui,
    vrm0_panel.VRM_PT_vrm0_blend_shape_master_armature_object_property,
    vrm0_panel.VRM_PT_vrm0_blend_shape_master_ui,
    vrm0_panel.VRM_PT_vrm0_first_person_armature_object_property,
    vrm0_panel.VRM_PT_vrm0_first_person_ui,
    vrm0_panel.VRM_PT_vrm0_secondary_animation_armature_object_property,
    vrm0_panel.VRM_PT_vrm0_secondary_animation_ui,
    vrm0_operator.VRM_OT_add_vrm0_first_person_mesh_annotation,
    vrm0_operator.VRM_OT_remove_vrm0_first_person_mesh_annotation,
    vrm0_operator.VRM_OT_add_vrm0_material_value_bind,
    vrm0_operator.VRM_OT_remove_vrm0_material_value_bind,
    vrm0_operator.VRM_OT_add_vrm0_material_value_bind_target_value,
    vrm0_operator.VRM_OT_remove_vrm0_material_value_bind_target_value,
    vrm0_operator.VRM_OT_add_vrm0_blend_shape_bind,
    vrm0_operator.VRM_OT_remove_vrm0_blend_shape_bind,
    vrm0_operator.VRM_OT_add_vrm0_secondary_animation_collider_group_collider,
    vrm0_operator.VRM_OT_remove_vrm0_secondary_animation_collider_group_collider,
    vrm0_operator.VRM_OT_add_vrm0_secondary_animation_group_bone,
    vrm0_operator.VRM_OT_remove_vrm0_secondary_animation_group_bone,
    vrm0_operator.VRM_OT_add_vrm0_secondary_animation_group_collider_group,
    vrm0_operator.VRM_OT_remove_vrm0_secondary_animation_group_collider_group,
    vrm0_operator.VRM_OT_add_vrm0_blend_shape_group,
    vrm0_operator.VRM_OT_remove_vrm0_blend_shape_group,
    vrm0_operator.VRM_OT_add_vrm0_secondary_animation_group,
    vrm0_operator.VRM_OT_remove_vrm0_secondary_animation_group,
    vrm0_operator.VRM_OT_add_vrm0_secondary_animation_collider_group,
    vrm0_operator.VRM_OT_remove_vrm0_secondary_animation_collider_group,
    # editor.detail_mesh_maker.ICYP_OT_detail_mesh_maker,
    glsl_drawer.ICYP_OT_draw_model,
    glsl_drawer.ICYP_OT_remove_draw_model,
    make_armature.ICYP_OT_make_armature,
    # editor.mesh_from_bone_envelopes.ICYP_OT_make_mesh_from_bone_envelopes,
    operator.VRM_OT_add_human_bone_custom_property,
    operator.VRM_OT_add_defined_human_bone_custom_property,  # deprecated
    operator.VRM_OT_add_extensions_to_armature,
    operator.VRM_OT_add_required_human_bone_custom_property,  # deprecated
    operator.VRM_OT_simplify_vroid_bones,
    operator.VRM_OT_vroid2vrc_lipsync_from_json_recipe,
    operator.VRM_OT_save_human_bone_mappings,
    operator.VRM_OT_load_human_bone_mappings,
    validation.VrmValidationError,
    export_scene.validation.WM_OT_vrm_validator,
    export_scene.VRM_PT_export_error_messages,
    export_scene.EXPORT_SCENE_OT_vrm,
    import_scene.LicenseConfirmation,
    import_scene.WM_OT_license_confirmation,
    import_scene.IMPORT_SCENE_OT_vrm,
    # importer.blend_model.ICYP_OT_select_helper,
    preferences.VrmAddonPreferences,
    vrm0_property_group.Vrm0PropertyGroup,
    extension.VrmAddonArmatureExtensionPropertyGroup,
]


# アドオン有効化時の処理
def register(init_version: Any) -> None:
    # Sanity check
    if init_version != version.version():
        raise Exception(
            f"Sanity error: version mismatch: {init_version} != {version.version()}"
        )

    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(import_scene.menu_import)
    bpy.types.TOPBAR_MT_file_export.append(export_scene.menu_export)
    bpy.types.VIEW3D_MT_armature_add.append(panel.add_armature)
    # bpy.types.VIEW3D_MT_mesh_add.append(panel.make_mesh)
    bpy.app.handlers.load_post.append(add_shaders)
    bpy.app.translations.register(
        preferences.addon_package_name,
        translation_dictionary,
    )
    bpy.types.Armature.vrm_addon_extension = bpy.props.PointerProperty(
        type=extension.VrmAddonArmatureExtensionPropertyGroup
    )


# アドオン無効化時の処理
def unregister() -> None:
    bpy.app.translations.unregister(preferences.addon_package_name)
    bpy.app.handlers.load_post.remove(add_shaders)
    bpy.types.VIEW3D_MT_armature_add.remove(panel.add_armature)
    # bpy.types.VIEW3D_MT_mesh_add.remove(panel.make_mesh)
    bpy.types.TOPBAR_MT_file_import.remove(import_scene.menu_import)
    bpy.types.TOPBAR_MT_file_export.remove(export_scene.menu_export)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    if hasattr(bpy.types.Armature, "vrm_addon_extension"):
        del bpy.types.Armature.vrm_addon_extension
    if hasattr(bpy.types.Bone, "vrm_addon_extension"):
        del bpy.types.Bone.vrm_addon_extension
    if hasattr(bpy.types.ShapeKey, "vrm_addon_extension"):
        del bpy.types.ShapeKey.vrm_addon_extension
