% 3D Layer Building Method 11/19
clear; clc;
warning('off','MATLAB:table:ModifiedAndSavedVarnames')

% Have user browse for a file, from a specified "starting folder."
% For convenience in browsing, set a starting folder from which to browse.
startingFolder = 'C:\Program Files\MATLAB';
if ~exist(startingFolder, 'dir')
  % If that folder doesn't exist, just start in the current folder.
  startingFolder = pwd;
end
% Get the name of the file that the user wants to use.
defaultFileName = fullfile(startingFolder, '*.*');
[baseFileName, folder] = uigetfile(defaultFileName, 'Select a file');
if baseFileName == 0
  % User clicked the Cancel button.
  return;
end
fullFileName = fullfile(folder, baseFileName);
% Now call your other m-file with this filename as an input argument:
data = readtable(fullFileName);

% Input crate and box dimensions
prompt = {'Number of Boxes 520mm x 400mm x 230mm','Number of Boxes 300mm x 210mm x 140mm'...
    'Number of Boxes 270mm x 195mm x 145mm' 'Number of Boxes 175mm x 150mm x 125mm'...
    'Number of Boxes 280mm x 210mm x 130mm'};
dlgtitle = 'Input';
dims = [1 35];
answer = inputdlg(prompt,dlgtitle,dims);

% String to number matrix
for p = 1:5
    num_box(p) = str2double(answer{p});
end
num_box = num_box.';

% Input number of iterations for program
question = {'Number of Iterations'};
title = 'Iterate';
dimz = [1 35];
it = inputdlg(question,title,dimz);
iterations = str2double(it{1});

% Total number of boxes
box_count = sum(num_box);

% Initialize box dimension matrix
box_dim = zeros(box_count,4);

% Actual box sixes used at Mobis
test_sizes = table2array([data(346,3:8); data(37,3:8); data(8,3:8); data(2,3:8); data(11,3:8)]);
height = [3;2;2;1;1];% Simplified Heights

% Fill correct box sizes into dimension matrix
counter = 1;
count = 1;
while counter <= box_count
    for i =  1: num_box(count)
        box_dim(counter,1) = test_sizes(count,1); % Length
        box_dim(counter,2) = test_sizes(count,2); % Width
        box_dim(counter,3) = height(count); % Height
        %box_dim(counter,3) = test_sizes(count,3); % Actual Height
        box_dim(counter,4) = box_dim(counter,1)*box_dim(counter,2)*box_dim(counter,3); % Volume
        %box_dim(counter,4) = test_sizes(count,4); % Actual Volume
        box_dim(counter,5) = test_sizes(count,6); % Weight
        counter = counter + 1;
    end
    count = count + 1;
end

% Actual crate dimensions used by Mobis
crate_dim = [1277,1087,10]; % crate_dim = [1277,1087,980]
V_crate = crate_dim(1)*crate_dim(2)*crate_dim(3);
sorted_dim = sortrows(box_dim,5,'descend');

% Number of boxes removed each time
num_removed = 2;

% Initialize variables
j = zeros(1,iterations);
X_box(:,1:iterations) = repmat(sorted_dim(:,1),1,iterations);
Y_box(:,1:iterations) = repmat(sorted_dim(:,2),1,iterations);
Z_box(:,1:iterations) = repmat(sorted_dim(:,3),1,iterations);
V_box = zeros(length(box_dim),iterations);
x_pos = zeros(length(box_dim),iterations);
y_pos = zeros(length(box_dim),iterations);
z_pos = zeros(length(box_dim),iterations);

tic
for n=1:iterations

    % Create set of sizes for boxes, using C sizes to correct sizes when boxes are reorientated
    Cx = sorted_dim(:,1)';
    Cy = sorted_dim(:,2)';
    Cz = sorted_dim(:,3)';

    % Create matrix of zeros to determine if space is occupied
    M = zeros(crate_dim(2),crate_dim(1));
    M(:,:,2:crate_dim(3)) = zeros(crate_dim(2),crate_dim(1),crate_dim(3)-1);

    % Initialize variables
    x = zeros(1,V_crate);
    y = zeros(1,V_crate);
    z = zeros(1,V_crate);
    removed_box = randi([1 length(box_dim)], iterations, num_removed); % Make so cant be repeat
    x(1) = 1;
    y(1) = 1;
    z(1) = 1;
    x_pos(1,n) = 1;
    y_pos(1,n) = 1;
    z_pos(1,n) = 1;
    j(1,n) = 1;

    while j(n)<=length(box_dim)

        if n > 1
            if ismember(j(n),removed_box(n,:))
                j(n) = j(n) + 1;
            end
        end

        if j(n) > length(box_dim)
            break
        end

        % Loop to check every single position within the crate for available space
        k = 1;
        for k = 1:V_crate

            % Check to see if position is occupied
            if M(y(k),x(k),z(k)) ~= 0
                x(k+1) = x(k) + 1;
                y(k+1) = y(k);
                z(k+1) = z(k);

                % Check if position is within crate dimensions
                if x(k+1) > crate_dim(1)
                    x(k+1) = 1;
                    y(k+1) = y(k) + 1;
                    z(k+1) = z(k);
                end
                if y(k+1) > crate_dim(2)
                    x(k+1) = 1;
                    y(k+1) = 1;
                    z(k+1) = z(k) + 1;
                end
                if z(k+1) > crate_dim(3)
                    break
                end

            else
                % Set box as its default orientation
                fill_x(k) = x(k) + Cx(j(n)) - 1;
                fill_y(k) = y(k) + Cy(j(n)) - 1;
                fill_z(k) = z(k) + Cz(j(n)) - 1;

                % If box fits in its current orientation, fill crate with box
                if fill_x(k) <= crate_dim(1) & fill_y(k) <= crate_dim(2) & fill_z(k) <= crate_dim(3) & ...
                        M(y(k):fill_y(k),x(k):fill_x(k),z(k):fill_z(k)) == 0
                    M(y(k):fill_y(k),x(k):fill_x(k),z(k):fill_z(k)) = j(n);
                    % Set coordinate position for box
                    x_pos(j(n),n) = x(k);
                    y_pos(j(n),n) = y(k);
                    z_pos(j(n),n) = z(k);
                    V_box(j(n),n) = X_box(j(n),n)*Y_box(j(n),n)*Z_box(j(n),n);
                    clear x y fill_x fill_y fill_z
                    k = 1;
                    x(k) = x_pos(j(n),n) + X_box(j(n),n);
                    y(k) = 1;
                    z(k) = z(k);

                    % If next position is outside of crate, go to next row
                    if x(k) > crate_dim(1)
                        x(k) = 1;
                    end
                    j(n) = j(n) + 1;

                    % End loop if all the boxes are placed in the crate
                    if n > 1
                        if ismember(j(n),removed_box(n,:))
                            j(n) = j(n) + 1;
                        end
                    end

                    if j(n) > length(box_dim)
                        break
                    end
                    break

                else
                    % Flip X and Y orientation of box
                    fill_x(k) = x(k) + Cy(j(n)) - 1;
                    fill_y(k) = y(k) + Cx(j(n)) - 1;

                    % If box fits in its new orientation, fill crate with box
                    if fill_x(k) <= crate_dim(1) & fill_y(k) <= crate_dim(2) & fill_z(k) <= crate_dim(3) & ...
                            M(y(k):fill_y(k),x(k):fill_x(k),z(k):fill_z(k))==0
                        M(y(k):fill_y(k),x(k):fill_x(k),z(k):fill_z(k)) = j(n);
                        % Set coordinate position for box
                        x_pos(j(n),n) = x(k);
                        y_pos(j(n),n) = y(k);
                        z_pos(j(n),n) = z(k);
                        X_box(j(n),n) = Cy(j(n));
                        Y_box(j(n),n) = Cx(j(n));
                        Z_box(j(n),n) = Cz(j(n));
                        V_box(j(n),n) = X_box(j(n),n)*Y_box(j(n),n)*Z_box(j(n),n);
                        clear x y fill_x fill_y fill_z
                        k = 1;
                        x(k) = x_pos(j(n),n) + X_box(j(n),n);
                        y(k) = 1;

                        % If next position is outside of crate, go to next row
                        if x(k) > crate_dim(1)
                            x(k) = 1;
                        end
                        j(n) = j(n) + 1;

                        if n > 1
                            if ismember(j(n),removed_box(n,:))
                                j(n) = j(n) + 1;
                            end
                        end

                        % End loop if all the boxes are placed in the crate
                        if j(n) > length(box_dim)
                            break
                        end
                        break
                    end
                end

                % Check to make sure next positions are within crate
                x(k+1) = x(k) + 1;
                y(k+1) = y(k);
                z(k+1) = z(k);
                if x(k+1) > crate_dim(1)
                    x(k+1) = 1;
                    y(k+1) = y(k) + 1;
                    % If layer is full, go to next layer
                    if y(k+1) > crate_dim(2)
                        y(k+1) = 1;
                        x(k+1) = 1;
                        z(k+1) = z(k) + 1;
                    end
                    if z(k+1) > crate_dim(3)
                        break
                    end
                end
            end

            % Go on to next box if available space not found for specific box
            if k == V_crate
                j(n) = j(n) + 1;
                if j(n) > length(box_dim)
                    break
                end
            end
        end
    end

    V_tot(n) = sum(V_box(:,n));
    V_used(n) = (V_tot(n) / V_crate) * 100;
end
toc

% Flip matrix to correct orientation
final_matrix = flip(M);

% Find orientation with max volume utilization
[vol_max,col_max] = max(V_used);
fprintf('%f percent volume usage \n',vol_max)

% Create 3D visualization of boxes loaded in crate
% plotcube.m(size matrix [X Y Z],origin location [X Y Z],1,'color code')
n = col_max;
for j = 1:length(x_pos)
    if x_pos(j,n) && y_pos(j,n) > 0 && z_pos(j,n) > 0
        plotcube( [crate_dim(1) crate_dim(2) crate_dim(3)], [0 0 0], .1, [0.9290 0.6940 0.1250]);
        plotcube( [X_box(j,n) Y_box(j,n) Z_box(j,n)], [x_pos(j,n)-1 y_pos(j,n)-1 z_pos(j,n)-1], 1, [rand rand rand])
    else
        % Create list of boxes not packed
        fprintf('Box %d not packed.\n',j)
    end
end
warning('on','all');
