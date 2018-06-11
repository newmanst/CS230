%run through all images obtain cell center 
%Output matrix with array [bx, by, bh, bw] <-- NOTE ORDER! 
% out = main('AugmentedImages/EOSINOPHIL');
% csvwrite('cellbounds_eosinophil.csv',out);

% out = main('AugmentedImages/NEUTROPHIL');
% csvwrite('cellbounds_neutrophil.csv',out);

% out = main('AugmentedImages/LYMPHOCYTE');
% csvwrite('cellbounds_lymphocyte.csv',out);

out = main('AugmentedImages/MONOCYTE');
csvwrite('cellbounds_monocyte.csv',out);
% get_cell_index('AugmentedImages/EOSINOPHIL/eosinophil_00000.png');

function [out] =  main(img_file)
   % xmin, ymin, xmax, ymax <-- (0,0) is top left corner
   out =  []; 
   files = dir(fullfile(img_file, '*.png'));
   allNames = {files.name} ; 
   for img_name=allNames
       img_path = strcat(img_file, '/', img_name);
       img_out = get_cell_index(img_path{1});
       out = [out; img_out];
   end
end

function [coords] = get_cell_index(image_path)

    % turn on display for debugging
    DISP = false;

    % read in image
    img = imread(image_path);
    imgsize = size(img); 

    % convert to double and devide channels
    [R, G, B] = divide_channels(img);

    % create custom gray level image and normalize
    gray_img = B-R-G;
    gray_img = gray_img - min(gray_img(:));
    gray_img = gray_img / max(gray_img(:));


    % binarize image
    gray_bin = imbinarize(gray_img, graythresh(gray_img));

    % remove small regions
    bin_cell = bwareaopen(gray_bin,750);
    
    % find bounding box
    [idx_y, idx_x] = ind2sub(size(bin_cell), find(bin_cell));
    py = min(idx_y);
    px = min(idx_x);
    bh = range(idx_y);
    bw = range(idx_x);
    bbox = [px, py, bw, bh];


    % display every step
    if DISP
        close all
        %figure()
        %imshow(img);

        %figure()
        %imshow(gray_img);

        %figure()
        %imshow(gray_bin);

        figure();
        imshow(bin_cell);
        hold on
        rectangle('Position', [px, py, bw, bh], 'EdgeColor', 'r');
%         plot(px, imgsize(1)-py-bh, "c*")
%         plot(px+bw, imgsize(1)-py, "co")
        plot(px, py, "c*")
        plot(px+bw, py+bh, "co")
  
    end
   
        % bring to one-hot
%     s = regionprops(bin_cell,'centroid');
%     cell_centroid = s.Centroid
%     idx = round(cell_centroid);

    bx = (px + bw/2) / imgsize(2);  %Normalized, (midpoint with 0,0 upper left) 
    by = (imgsize(1) - (py + bh/2) ) /imgsize(1);  %Normalized, (midpoint with 0,0 upper left) 
    bh_norm = bh/imgsize(1);
    bw_norm = bw/imgsize(2);
    
    out = [bx, by, bh_norm, bw_norm];
 %   coords = [px, imgsize(1)-py-bh, px+bw, imgsize(1)-py] % 0,0 is top left
    coords = [px, py, px+bw, py+bh] % 0,0 is bottom left 
%      rectangle('Position', coords, 'EdgeColor', 'b');

    function [R,G,B] = divide_channels(img)
        img = im2double(img);
        R = img(:,:,1);
        G = img(:,:,2);
        B = img(:,:,3);
    end

end