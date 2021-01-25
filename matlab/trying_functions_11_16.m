% Layer Building Method
clear; clc;
 
% Input crate and box dimensions

prompt = {'Number of Boxes 520mm x 230mm','Number of Boxes 300mm x 140mm'...
   'Number of Boxes 270mm x 145mm' 'Number of Boxes 175mm x 125mm'...
   'Number of Boxes 280mm x 130mm'};
dlgtitle = 'Input';
dims = [1 35];
answer = inputdlg(prompt,dlgtitle,dims);

% string to number matrix
for p = 1:5
   num_box(p) = str2num(answer{p});
end
num_box = num_box.';

question = {'Number of Iterations'};
title = 'Iterate';
dimz = [1 35];
it = inputdlg(question,title,dimz);
z = str2num(it{1});

% total number of boxes
box_count = sum(num_box);

% initialize box dimension matrix
box_dim = zeros(box_count,2);

% actual box sixes used at Mobis
test_sizes = [520,230;300,140;270,145;175,125;280,130];


% fill correct box sizes into dimension matrix
counter = 1;
count = 1;
while counter < box_count
    for i =  1: num_box(count)
        box_dim(counter,1) = test_sizes(count,1);
        box_dim(counter,2) = test_sizes(count,2);
        box_dim(counter,3) = box_dim(counter,1)*box_dim(counter,2);
        box_dim(counter,4) = test_sizes(count,2)/test_sizes(count,1);
        counter = counter + 1;
    end
    count = count + 1;
end

% actual crate dimensions used by Mobis
crate_dim = [1277,1087,1];
V_crate(1) = crate_dim(1)*crate_dim(2)*crate_dim(3);
sorted_dim = sortrows(box_dim,2,'descend');



%number of boxes removed each time
num_removed = 2;

%initialize real dimension matrix
x_fr = zeros(length(box_dim))';
y_fr = zeros(length(box_dim))';

tic
for n=1:z
     
    j(n) = 1;
    M = zeros(crate_dim(2),crate_dim(1));
    removed_box = randi([1 length(box_dim)], z, num_removed);

    
    while j(n)<=length(box_dim)
        
        if n > 1
            if ismember(j(n),removed_box(n,:))
                j(n) = j(n) + 1;
            else
                [x_out,y_out,M,V_bout,X_bout,Y_bout] = spot_finder(sorted_dim,crate_dim,j(n),M);
                x_pout(j(n)) = x_out;
                y_pout(j(n)) = y_out;
                M = M;
                V_boxout(j(n)) = V_bout;
                X_boxout(j(n)) = X_bout;
                Y_boxout(j(n)) = Y_bout;
                j(n) = j(n) + 1;
            end
        elseif n == 1
            [x_out,y_out,M,V_bout,X_bout,Y_bout] = spot_finder(sorted_dim,crate_dim,j(n),M);
            x_pout(j(n)) = x_out;
            y_pout(j(n)) = y_out;
            M = M;
            V_boxout(j(n)) = V_bout;
            X_boxout(j(n)) = X_bout;
            Y_boxout(j(n)) = Y_bout;
            j(n) = j(n) + 1;
        end
        
        if j(n) > length(box_dim)
            break
        end

    end
    
    if length(x_fr) ~= length(x_pout)
            diff = length(x_pout) - length(x_fr);
            x_pout(length(x_pout)-diff:length(x_pout)) = 0;
    end
    
    if n == 1
        V_tot(n) = sum(V_boxout);
        V_max(n) = (V_tot(n)/V_crate)*100;
        
        x_fr = x_pout;
        y_fr = y_pout;
        X_FR = X_boxout;
        Y_FR = Y_boxout;
    end
    
    if n > 1 
        V_tot(n) = sum(V_boxout);
        V_used(n) = (V_tot(n)/V_crate)*100;
        V_left = V_crate - V_used(n);
        
        for q=1:length(removed_box)
            box_no = removed_box(q,1);
            box_vol = sorted_dim(box_no,3);
    
            if box_vol < V_left
                [x_out,y_out,M,V_bout,X_bout,Y_bout] = spot_finder(sorted_dim,crate_dim,box_no,M);
                x_pout(box_no) = x_out;
                y_pout(box_no) = y_out;
                M = M;
                V_boxout(box_no) = V_bout;
                X_boxout(box_no) = X_bout;
                Y_boxout(box_no) = Y_bout;
                q = q + 1;
            else
                q = q + 1;
            end
        end
        
        V_tot(n) = sum(V_boxout);
        V_used(n) = (V_tot(n)/V_crate)*100;
        
        if V_used(n) > V_max(n-1)
            V_max(n) = V_used(n);
            x_fr = x_pout;
            y_fr = y_pout;
            X_FR = X_boxout;
            Y_FR = Y_boxout;
        else
            x_fr = x_fr;
            y_fr = y_fr;
            X_FR = X_FR;
            Y_FR = Y_FR;
            V_max(n) = V_max(n-1);
        end
        
    end
        
clear x_pout y_pout V_boxout M                   
end
toc

 
% Create 3D visualization of boxes loaded in crate
% plotcube.m(size matrix [X Y Z],origin location [X Y Z],1,'color code')
X = find(isnan(x_fr));
Y = find(isnan(y_fr));
x_fr(X) = 0;
y_fr(Y) = 0;

num = 0;

for j=1:length(x_fr)
    
    if x_fr(j) && y_fr(j) > 0
        plotcube( [crate_dim(1) crate_dim(2) crate_dim(3)], [0 0 0], .1, [0.9290 0.6940 0.1250]);
        plotcube( [X_FR(j) Y_FR(j) 1], [x_fr(j)-1 y_fr(j)-1 0], 1, [rand rand rand])
        V_fr(j) = X_FR(j)*Y_FR(j)*1;
        num = num + 1;
    else
        % Create list of boxes not packed
        fprintf('Box %d not packed.\n',j)
        j = j +1;
        num = num;
    end
end

% Continue list of boxes not packed
if length(x_fr) < length(box_dim)
    notpacked = (length(x_fr) + 1):length(box_dim);
    fprintf('Box %d not packed.\n',notpacked)
end

np = box_count - num;
fprintf('%d boxes not packed. \n', np)

V_tot = sum(V_fr);
V_used = (V_tot/V_crate)*100;
fprintf('%d percent volume usage \n',round(V_used))
