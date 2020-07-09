Abstract
One of the most frequently used types of digital image forgery is copying one area in
the image and pasting it into another area of the same image; this is known as the copy-
move forgery. To overcome the limitations of the existing Block-based and Keypoint-based
copy-move forgery detection methods, in this paper, we present an effective technique
for copy-move forgery detection that utilizes the image blobs and keypoints. The pro-
posed method is based on the image blobs and Binary Robust Invariant Scalable Keypoints
(BRISK) feature. It involves the following stages: the regions of interest called image blobs
and BRISK feature are found in the image being analyzed; BRISK keypoints that are located
within the same blob are identified; finally, the matching process is performed between
BRISK keypoints that are located in different blobs to find similar keypoints for copy-move
regions. The proposed method is implemented and evaluated on the copy-move forgery stan-
dard datasets MICC-F8multi, MICC-F220, and CoMoFoD. The experimental results show
that the proposed method is effective for geometric transformation, such as scaling and rota-
tion, and shows robustness to post-processing operation, such as noise addition, blurring,
and jpeg compression.
Keywords BRISK · Blob · CMF · CMFD · DoG · LoG
