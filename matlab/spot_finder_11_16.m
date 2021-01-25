function [x_pos,y_pos,M,V_box,X_box,Y_box] = spot_finder(sorted_dim,crate_dim,j,M)

V_crate = crate_dim(1)*crate_dim(2);

Cx = sorted_dim(:,1)';
Cy = sorted_dim(:,2)';
X_box = sorted_dim(:,1)';
Y_box = sorted_dim(:,2)';

% Initialize variables
clear x y x_pos y_pos k
x(1) = 1;
y(1) = 1;
x_pos(1) = 1;
y_pos(1) = 1;
k = 1;

for k = 1:V_crate
    
    if M(y(k),x(k)) ~= 0
       x(k+1) = x(k) + 1;
       y(k+1) = y(k);
       
       if x(k+1) > crate_dim(1)
           x(k+1) = 1;
           y(k+1) = y(k) + 1;
       end
       if y(k+1) > crate_dim(2)
           x_pos = NaN;
           y_pos = NaN;
           j = j + 1;
           V_box = 0;
           X_box = NaN;
           Y_box = NaN;
           M = M;
           break
       end
       
    else
         % Set box as its default orientation
        fill_x(k) = x(k) + Cx(j) - 1;
        fill_y(k) = y(k) + Cy(j) - 1;
        
        if fill_x(k) <= crate_dim(1) & fill_y(k) <= crate_dim(2) & M(y(k):fill_y(k),x(k):fill_x(k)) == 0
            M(y(k):fill_y(k),x(k):fill_x(k)) = j;
            x_pos = x(k);
            y_pos = y(k);
            X_box = X_box(j);
            Y_box = Y_box(j);
            V_box = sorted_dim(j,3);
            j = j + 1;
            break
            
        else
            % Flip orientation of box
            fill_x(k) = x(k) + Cy(j) - 1;
            fill_y(k) = y(k) + Cx(j) - 1;

            % If box fits in its new orientation, fill crate with box
            if fill_x(k) <= crate_dim(1) & fill_y(k) <= crate_dim(2) & M(y(k):fill_y(k),x(k):fill_x(k))==0
                M(y(k):fill_y(k),x(k):fill_x(k)) = j;
                % Set coordinate position for box
                x_pos = x(k);
                y_pos = y(k);
                X_box = Cy(j);
                Y_box = Cx(j);
                V_box = sorted_dim(j,3);
                j = j + 1;
                break
            end
            
        end
        
           x(k+1) = x(k) + 1;
           y(k+1) = y(k);
           if x(k+1) > crate_dim(1)
               x(k+1) = 1;
               y(k+1) = y(k) + 1;
           end
           if y(k+1) > crate_dim(2)
               x_pos = NaN;
               y_pos = NaN;
               j = j + 1;
               V_box = 0;
               X_box = NaN;
               Y_box = NaN;
               M = M;
               break
            end
        
        if k == V_crate
            x_pos = NaN;
           y_pos = NaN;
           j = j + 1;
           V_box = 0;
           X_box = NaN;
           Y_box = NaN;
           M = M;
           break
        end
    end
end
end
