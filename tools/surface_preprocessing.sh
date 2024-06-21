#!/bin/zsh

path_to_data=''
output_folder_separate=''
output_folder_resample='/'


for subjid in $( cat <./list_subjects.csv) ; do 

echo ${subjid}

### cifti separate
#cifti separate 
wb_command -cifti-separate ${path_to_data}/${subjid}.corrThickness.32k_fs_LR.dscalar.nii COLUMN  -metric CORTEX_LEFT ${output_folder_separate}/${subjid}.corrThickness.32k_fs_LR.L.shape.gii

wb_command -cifti-separate ${path_to_data}/${subjid}.corrThickness.32k_fs_LR.dscalar.nii COLUMN -metric CORTEX_RIGHT ${output_folder_separate}/${subjid}.corrThickness.32k_fs_LR.R.shape.gii

wb_command -cifti-separate ${path_to_data}/${subjid}.curvature.32k_fs_LR.dscalar.nii COLUMN -metric CORTEX_LEFT ${output_folder_separate}/${subjid}.curvature.32k_fs_LR.L.shape.gii

wb_command -cifti-separate ${path_to_data}/${subjid}.curvature.32k_fs_LR.dscalar.nii COLUMN -metric CORTEX_RIGHT ${output_folder_separate}/${subjid}.curvature.32k_fs_LR.R.shape.gii

wb_command -cifti-separate ${path_to_data}/${subjid}.MyelinMap_BC.32k_fs_LR.dscalar.nii COLUMN -metric CORTEX_LEFT ${output_folder_separate}/${subjid}.MyelinMap_BC.32k_fs_LR.L.shape.gii

wb_command -cifti-separate ${path_to_data}/${subjid}.MyelinMap_BC.32k_fs_LR.dscalar.nii COLUMN -metric CORTEX_RIGHT ${output_folder_separate}/${subjid}.MyelinMap_BC.32k_fs_LR.R.shape.gii

wb_command -cifti-separate ${path_to_data}/${subjid}.sulc.32k_fs_LR.dscalar.nii COLUMN -metric CORTEX_LEFT ${output_folder_separate}/${subjid}.sulc.32k_fs_LR.L.shape.gii

wb_command -cifti-separate ${path_to_data}/${subjid}.sulc.32k_fs_LR.dscalar.nii COLUMN -metric CORTEX_RIGHT ${output_folder_separate}/${subjid}.sulc.32k_fs_LR.R.shape.gii

## merge 

wb_command -metric-merge ${output_folder_separate}/${subjid}_R.shape.gii -metric  ${output_folder_separate}/${subjid}.MyelinMap_BC.32k_fs_LR.R.shape.gii -metric ${output_folder_separate}/${subjid}.curvature.32k_fs_LR.R.shape.gii -metric  ${output_folder_separate}/${subjid}.corrThickness.32k_fs_LR.R.shape.gii  -metric  ${output_folder_separate}/${subjid}.sulc.32k_fs_LR.R.shape.gii
wb_command -metric-merge ${output_folder_separate}/${subjid}_L.shape.gii -metric  ${output_folder_separate}/${subjid}.MyelinMap_BC.32k_fs_LR.L.shape.gii -metric ${output_folder_separate}/${subjid}.curvature.32k_fs_LR.L.shape.gii -metric  ${output_folder_separate}/${subjid}.corrThickness.32k_fs_LR.L.shape.gii  -metric  ${output_folder_separate}/${subjid}.sulc.32k_fs_LR.L.shape.gii

## resample

wb_command -metric-resample ${output_folder_separate}/${subjid}_R.shape.gii  ./Q1-Q6_RelatedParcellation210.R.sphere.32k_fs_LR.surf.gii ./Q1-Q6_RelatedParcellation210.R.sphere.ico6_fs_LR.surf.gii BARYCENTRIC ${output_folder_resample}/${subjid}_R.shape.gii
wb_command -metric-resample ${output_folder_separate}/${subjid}_L.shape.gii  ./Q1-Q6_RelatedParcellation210.L.sphere.32k_fs_LR.surf.gii ./Q1-Q6_RelatedParcellation210.L.sphere.ico6_fs_LR.surf.gii BARYCENTRIC ${output_folder_resample}/${subjid}_L.shape.gii

## set left structure
wb_command -set-structure  ${output_folder_resample}/${subjid}_R.shape.gii CORTEX_LEFT
wb_command -set-structure  ${output_folder_resample}/${subjid}_L.shape.gii CORTEX_LEFT

done

