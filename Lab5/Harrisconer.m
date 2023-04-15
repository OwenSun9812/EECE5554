clc
clear all
close all
K=load('Exter_Param1.mat');
cameraParams=K.cameraParams1;

% buildingDir = fullfile('./picture/h15');
buildingDir = fullfile('./picture/h50');
% buildingDir = fullfile('./picture/15%');
buildingScene = imageDatastore(buildingDir);

montage(buildingScene.Files)


ac = readimage(buildingScene,1);
ac = undistortImage(ac,cameraParams,'OutputView','valid');
ac=imresize(ac,0.5);
% figure;imshow(I);
% I=imrotate(I,-90);

grayI = rgb2gray(ac);
[k,h,n] = harris(grayI,4500,'tile',[2 2],'disp');
po=[h,k];

% points = detectSURFFeatures(grayImage);
[fea, po] = extractFeatures(grayI, po);

% Initialize all the transforms to the identity matrix. Note that the
% projective transform is used here because the building images are fairly
% close to the camera. Had the scene been captured from a further distance,
% an affine transform would suffice.
numI = numel(buildingScene.Files);
tforms(numI) = projective2d(eye(3));

% Initialize variable to hold image sizes.
imageS = zeros(numI,2);

% Iterate over remaining image pairs
for n = 2:numI
    
    % Store points and features for I(n-1).
    pointsPrevious = po;
    featuresPrevious = fea;
        
    % Read I(n).
    ac = readimage(buildingScene, n);
    ac = undistortImage(ac,cameraParams,'OutputView','valid');
%     figure;imshow(I);
    ac=imresize(ac,0.5);
%     I=imrotate(I,-90);

    % Convert image to grayscale.
    grayI = rgb2gray(ac);    
    
    % Save image size.
    imageS(n,:) = size(grayI);
    
    % Detect and extract SURF features for I(n).
%     points = detectSURFFeatures(grayImage);   
    [k,h,n] = harris(grayI,5000,'tile',[2 2],'disp');
    po=[h,k];
    [fea, po] = extractFeatures(grayI, po);
  
    % Find correspondences between I(n) and I(n-1).
    indP = matchFeatures(fea, featuresPrevious,'Unique', true,'MatchThreshold',1);
       
    matcP = po(indP(:,1), :);
    matPP = pointsPrevious(indP(:,2), :);        
    
    % Estimate the transformation between I(n) and I(n-1).
    tforms(n) = estimateGeometricTransform(matcP, matPP,...
        'projective', 'Confidence', 99.9, 'MaxNumTrials', 2000);
    
    % Compute T(n) * T(n-1) * ... * T(1)
    tforms(n).T = tforms(n).T * tforms(n-1).T; 
end

% Compute the output limits  for each transform
for i = 1:numel(tforms)           
    [xlim(i,:), ylim(i,:)] = outputLimits(tforms(i), [1 imageS(i,2)], [1 imageS(i,1)]);    
end


avgXLm = mean(xlim, 2);

[~, idx] = sort(avgXLm);

centerId = floor((numel(tforms)+1)/2);

centerIId = idx(centerId);

Tinv = invert(tforms(centerIId));

for i = 1:numel(tforms)    
    tforms(i).T = tforms(i).T * Tinv.T;
end


for i = 1:numel(tforms)           
    [xlim(i,:), ylim(i,:)] = outputLimits(tforms(i), [1 imageS(i,2)], [1 imageS(i,1)]);
end

maxImageSize = max(imageS);


xMina = min([1; xlim(:)]);
xMaxa = max([maxImageSize(2); xlim(:)]);

yMinb = min([1; ylim(:)]);
yMaxb = max([maxImageSize(1); ylim(:)]);


wid  = round(xMaxa - xMina);
hei = round(yMaxb - yMinb);


panor = zeros([hei wid 3], 'like', ac);
blender = vision.AlphaBlender('Operation', 'Binary mask', ...
    'MaskSource', 'Input port');  


xLi = [xMina xMaxa];
yLi = [yMinb yMaxb];
panoView = imref2d([hei wid], xLi, yLi);


for i = 1:numI
    
    ac = readimage(buildingScene, i);  
    ac = undistortImage(ac,cameraParams,'OutputView','valid');
%     figure;imshow(I);
    ac=imresize(ac,0.5);
%     I=imrotate(I,-90);
   
    % Transform I into the panorama.
    warpIma = imwarp(ac, tforms(i), 'OutputView', panoView);
                  
    % Generate a binary mask.    
    masks = imwarp(true(size(ac,1),size(ac,2)), tforms(i), 'OutputView', panoView);
    
    % Overlay the warpedImage onto the panorama.
    panor = step(blender, panor, warpIma, masks);
end

figure
imshow(panor)