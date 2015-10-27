"""
Region Extraction using a t-statistical maps (3D)
=================================================

This example shows how to extract regions or seperate the regions
from the statistical maps.

We use localizer t-statistic maps as an input image.

The idea is to threshold an input for foreground objects using a
function `foreground_extraction` and extract foreground objects using a
function `connected_components_extraction`.

In this example, we also show how to use raw t-statistical value as a
threshold and extract regions based on survived foreground objects.

This example is particular to the use case of target specific
region of interest analysis.
"""

# Load localizer datasets - contrast/t maps
from nilearn import datasets
from nilearn._utils import check_niimg_3d
print(" -- Fetching t-statistic image from localizer datasets -- ")
n_subjects = 1
localizer_path = datasets.fetch_localizer_contrasts(
    ['calculation (auditory cue)'], n_subjects=n_subjects, get_tmaps=True)
localizer_img = check_niimg_3d(localizer_path.tmaps[0])

# Thresholding the input image
from nilearn.regions import region_extractor
print(" -- Thresholding the image -- ")
# Thresholding based on (ratio * n_voxels) named as "ratio_n_voxels"
localizer_threshold_img = region_extractor.foreground_extraction(
    localizer_img, threshold=0.1, thresholding_strategy='ratio_n_voxels')

# Thresholding based on raw t-statistical values
localizer_threshold_tstat_img = region_extractor.foreground_extraction(
    localizer_img, threshold=4., thresholding_strategy=None)

# Region extraction/seperation
print(" -- Region Extraction/Seperation -- ")
# Region extraction based on only labelling named as "connected_components"
regions_cc = region_extractor.connected_component_extraction(
    localizer_threshold_img, min_size=200, extract_type='connected_components')
n_regions_cc = len(regions_cc)

# Region extraction based on Random Walker Segmentation algorithm named as
# "local_regions"
regions_rwe = region_extractor.connected_component_extraction(
    localizer_threshold_img, min_size=200, extract_type='local_regions')
n_regions_rwe = len(regions_rwe)

# Region extraction on a t-statistic value based on threshold image
regions_tstat = region_extractor.connected_component_extraction(
    localizer_threshold_tstat_img, min_size=200)
n_regions_tstat = len(regions_tstat)

# Visualization
print(" -- Showing the results -- ")
import matplotlib.pyplot as plt
from nilearn import plotting
# Visualize input t map
plotting.plot_stat_map(localizer_img, title='Input_data: Statistical t-map')

# Visualize thresholded t-maps
title = ('Statistical t-map after thresholding'
         ' \nusing a standard procedure')
plotting.plot_stat_map(localizer_threshold_img, title=title)
title = ('Statistical t-map after thresholding'
         ' \nusing t-value')
plotting.plot_stat_map(localizer_threshold_tstat_img, title=title)

# Visualize region extraction images
title = ('n_regions=%d are extracted from a "t value" based threshold'
         ' \nEach color identifies a seperate region' % n_regions_tstat)
plotting.plot_prob_atlas(regions_tstat, view_type='filled_contours',
                         title=title)
title = ('Region Extraction results of "t-statistic threshold" value'
         ' overlayed onto a input raw statistical image')
plotting.plot_prob_atlas(regions_tstat, anat_img=localizer_img,
                         view_type='contours', display_mode='z', cut_coords=1,
                         title=title)

title = ('n_regions=%d are extracted from a "connected components" procedure'
         ' \nEach color identifies a seperate region' % n_regions_cc)
plotting.plot_prob_atlas(regions_cc, view_type='filled_contours',
                         title=title)
title = ('Region Extraction results of "connected components" '
         'overlayed onto a input raw statistical image')
plotting.plot_prob_atlas(regions_cc, anat_img=localizer_img,
                         view_type='contours', display_mode='z',
                         cut_coords=5, title=title)

title = ('n_regions=%d are extracted from a "random walker" procedure'
         ' \nEach color identifies a seperate region' % n_regions_rwe)
plotting.plot_prob_atlas(regions_rwe, view_type='filled_contours',
                         title=title)
title = ('Region Extraction results of "random walker" procedure '
         'overlayed onto a input raw statistical image')
plotting.plot_prob_atlas(regions_rwe, anat_img=localizer_img,
                         view_type='contours', display_mode='z',
                         cut_coords=5, title=title)

plt.show()
