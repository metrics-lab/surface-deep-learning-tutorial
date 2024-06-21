## OHBM 2024 - Surface Deep Learning Tutorial

This repository contains the codebase for the surface deep learning tutorial at the [OHBM2024 Educational Symposium on Precision Surface Imaging](https://metrics-lab.github.io/ohbm2024/).

Here, we introduce the tools to prepare surface data for surface deep learning. In particular, we detail the preprocessing steps to prepare cortical metrics and functional data in order to use the Surface Vision Transformer [SiT](https://arxiv.org/abs/2203.16414) and the Multiscale Surface Vision Transformer [MS-SiT](https://arxiv.org/abs/2303.11909) for cortical prediction & classification and cortical segmentation tasks.

<img src="./docs/sit_gif.gif"
     alt="Surface Vision Transformers"
     style="float: left; margin-right: 10px;" />


# 1. Installation & Set-up

## A. Connectome Workbench

Connectome Workbench is a free software for visualising neuroimaging data and can be used for visualising cortical metrics on surfaces. Downloads and instructions [here](https://www.humanconnectome.org/software/connectome-workbench). 

## B. Conda usage

For PyTorch and dependencies installation with conda, please follow instructions in [install.md](docs/install.md).

## C. Docker usage

For docker support, please follow instructions in [docker.md](docs/docker.md)


# 2. Data Preprocessing & Access to Preprocessed Data

To simplify reproducibility of our work, data already preprocessed as in in [S. Dahan et al 2021](https://arxiv.org/abs/2203.16414) is available (see Section B). Otherwise, the following guideline provide the  preprocessing steps for custom datasets (Section A).

## A. Data preprocessing for Surface Deep Learning

The following methodology is intended for processing CIFTI files into cortical metrics and functional data in the format `shape.gii` and `func.gii`, for deep learning usage. We provide a bash script to recapitulate all the main preprocessing steps in `./tools/surface_preprocessing.sh`. Below are the instructions for each step in the script. 

### Step-by-Step Instruction

a. CIFTI separation

First, we separate the CIFTI files in the format `dscalar.nii` into individual cortical metrics for the left and right hemispheres. This is done using the workbench command `-cifti-separate`. Each metric (e.g., cortical thickness, curvature, MyelinMap_BC, sulcal depth) is saved as a `.shape.gii` file.

```
wb_command -cifti-separate ${path_to_data}/${subjid}.corrThickness.32k_fs_LR.dscalar.nii COLUMN -metric CORTEX_LEFT ${output_folder_separate}/${subjid}.corrThickness.32k_fs_LR.L.shape.gii
wb_command -cifti-separate ${path_to_data}/${subjid}.corrThickness.32k_fs_LR.dscalar.nii COLUMN -metric CORTEX_RIGHT ${output_folder_separate}/${subjid}.corrThickness.32k_fs_LR.R.shape.gii

```

b. Merge Metrics: 

Then, we merge the individual metric files into a single file for each hemisphere using the workbench `-metric-merge`. This combines multiple cortical metrics into one .shape.gii file for each hemisphere.


```
wb_command -metric-merge ${output_folder_separate}/${subjid}_R.shape.gii -metric ${output_folder_separate}/${subjid}.MyelinMap_BC.32k_fs_LR.R.shape.gii -metric ${output_folder_separate}/${subjid}.curvature.32k_fs_LR.R.shape.gii -metric ${output_folder_separate}/${subjid}.corrThickness.32k_fs_LR.R.shape.gii -metric ${output_folder_separate}/${subjid}.sulc.32k_fs_LR.R.shape.gii

wb_command -metric-merge ${output_folder_separate}/${subjid}_L.shape.gii -metric ${output_folder_separate}/${subjid}.MyelinMap_BC.32k_fs_LR.L.shape.gii -metric ${output_folder_separate}/${subjid}.curvature.32k_fs_LR.L.shape.gii -metric ${output_folder_separate}/${subjid}.corrThickness.32k_fs_LR.L.shape.gii -metric ${output_folder_separate}/${subjid}.sulc.32k_fs_LR.L.shape.gii

```

c. Metric resampling

Then, we resample the metrics to a standard icosahedral mesh (ico6) using the wb_command `-metric-resample` command. This ensures all metrics are aligned to a common spherical surface for consistent analysis. We provide ico6 meshes for both hemispheres in the folder `./surfaces`. These icospheres work with our triangular mesh patching. 

```
wb_command -metric-resample <metric-in> <current-sphere> <new-sphere> BARYCENTRIC <metric-out>
```

Where `<metric-in>` is the input metric or functional file, `<new-sphere>` being the ico6 sphere provided, `<current-sphere>` the sphere the input metric is currently registered to. 

For further details about the `metric-resample` command please follow [this](https://www.humanconnectome.org/software/workbench-command/-metric-resample).



<img src="./docs/Icosphere_Levels.png"
alt="Surface Vision Transformers"
style="float: left; margin-right: 6px;"/>


If the original input data, is low resolution, it can be resampled to higher resolution sequentially. For this we provide the icoN resolution surfaces. For instance:

```
wb_command -metric-resample <metric-in> ico-1.L.surf.gii ico-2.L.surf.gii BARYCENTRIC <metric-out>
wb_command -metric-resample <metric-in> ico-2.L.surf.gii ico-3.L.surf.gii BARYCENTRIC <metric-out>
etc.
```


d. Setting Cortex Left structure

For surface deep learning, by convention. right hemispheres are flipped such that they appear like right hemisphere on the sphere and all hemispheres are processed altogether in the training pipelines. 

Therefore you can set the structure of the resampled metrics to CORTEX_LEFT for both hemispheres using the wb_command `-set-structure` command. This standardises the hemisphere structure for subsequent analysis.

```
for i in *; do wb_command -metric-resample ${i} ../ico-6.L.surf.gii BARYCENTRIC ${i}; done
```

Once symmetrised, both left and right hemispheres have the same orientation when visualised on a left hemipshere template. 
<img src="./docs/left_right_example.png"
alt="Surface Vision Transformers"
style="float: left; margin-right: 6px;"/>

e. (optional) Patching surface data

To run the Surface Vision Transformers, there are two possible approaches, (1) either preprocessed the metrics files to create numpy array with all the compiled data, or (2) use a custom-made dataset/dataloader which offer more flexibility in terms of data processing and data augmentation techniques. 

To prepare the data in `option 1`, you can use the YAML file `config/preprocessing/hparams.yml`, change the path to data, set the parameters and run the `./tools/preprocessing.py` script in ./tools:

```
cd tools
python preprocessing.py ../config/preprocessing/hparams.yml
```



## B. (Optional) Accessing processed data

Cortical surface metrics already processed as in [S. Dahan et al 2021](https://arxiv.org/abs/2203.16414) and [A. Fawaz et al 2021](https://www.biorxiv.org/content/10.1101/2021.12.01.470730v1) are available upon request. 

<details>
    <summary><b> How to access the processed data?</b></summary>
    <p>
    To access the data please:
    <br>
        <ul type="circle">
            <li> Sign the dHCP open access agreement [here](https://www.developingconnectome.org/data-release/second-data-release/open-access-dhcp-data-terms-of-use-version-4-0_2019-05-23/) </li>
            <li> Create a [GIN](https://gin.g-node.org/) account </li>
            <li> Send your GIN username with the dHCP signed form to <b> simon.dahan@kcl.ac.uk</b>  </li>
        </ul>
    </br>
    </p>
</details>
<details>
  <summary><b> G-Node GIN repository</b></summary>
      <p>
      Once the confirmation has been sent, you will have access to the <b>G-Node GIN repository</b> containing the data already processed.
      The data used for this project is in the zip files <i>`regression_native_space_features.zip`</i> and <i>`regression_template_space_features.zip`</i>. You also need to use the <i>`ico-6.surf.gii`</i> spherical mesh.
      </br>
      <img src="./docs/g_node.png"
        alt="Surface Vision Transformers"
        width="400" 
        height="300"
        style="float: left; margin-right: 6px;"/>
</details>

**Training** and **validation** sets are available for the task of **birth-age** and **scan-age** prediction, in **template** and **native** configuration.

However the test set is not currently publicly available as used as testing set in the [SLCN challenge](https://slcn.grand-challenge.org/) on surface learning alongside the MLCN workshop at MICCAI 2022. 

# 3. Model Zoo

Here is a list of available pre-trained models on various datasets.

| Dataset | Surface Vision Transformer (SiT) | Multiscale Surface Vision Transformer (MS-SiT) |
|---------|----------------------------------|------------------------------------------------|
| dHCP (cortical metrics)   | [Scan Age Prediction](http://example.com/sit-dhcp) / [Birth Age Prediction](http://example.com/sit-dhcp) | [Scan Age Prediction](http://example.com/sit-dhcp) / [Birth Age Prediction](http://example.com/sit-dhcp)|
| UKB (cortical metrics)    |  [Scan Age Prediction](http://example.com/sit-dhcp) / [Sex Classification](http://example.com/sit-dhcp)  | [Scan Age Prediction](http://example.com/sit-dhcp) / [Sex Classification](http://example.com/sit-dhcp)  |
| HCP (3T - cortical metrics)    |  [Scan Age Prediction](http://example.com/sit-dhcp) / [Sex Classification](http://example.com/sit-dhcp)  |  [Scan Age Prediction](http://example.com/sit-dhcp) / [Sex Classification](http://example.com/sit-dhcp)  |


# Citation

Please cite these works if you found it useful:

[Surface Vision Transformers: Attention-Based Modelling applied to Cortical Analysis](https://arxiv.org/abs/2203.16414)

```
@article{dahan2022surface,
  title={Surface Vision Transformers: Attention-Based Modelling applied to Cortical Analysis},
  author={Dahan, Simon and Fawaz, Abdulah and Williams, Logan ZJ and Yang, Chunhui and Coalson, Timothy S and Glasser, Matthew F and Edwards, A David and Rueckert, Daniel and Robinson, Emma C},
  journal={arXiv preprint arXiv:2203.16414},
  year={2022}
}
```
[The Multiscale Surface Vision Transformer](https://arxiv.org/abs/2204.03408)

```
@article{dahan2022surface,
  title={Surface Vision Transformers: Flexible Attention-Based Modelling of Biomedical Surfaces},
  author={Dahan, Simon and Xu, Hao and Williams, Logan ZJ and Fawaz, Abdulah and Yang, Chunhui and Coalson, Timothy S and Williams, Michelle C and Newby, David E and Edwards, A David and Glasser, Matthew F and others},
  journal={arXiv preprint arXiv:2204.03408},
  year={2022}
}
```


