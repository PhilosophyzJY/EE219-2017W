% Read in data %
[data,text] = xlsread('RMF.xlsx');
users = max(data(:,1)); % number of users
movies = max(data(:,2)); % number of movies

% Initialization %
R = zeros(users,movies);
W = zeros(users,movies);

% Construct R 0-1 matrix and rating W matrix %
for x = 1:size(data,1)
    R(data(x,1),data(x,2)) = 1;
    W(data(x,1),data(x,2)) = data(x,3);
end

% Pick top L movies for each user %
L = 5;
topL = zeros(users,L);

% Generate 10-Fold CV indices %
indices = crossvalind('Kfold',size(data,1), 10);
a = 1;

for n = 1:10
    % Setting nth fold data to 0 %
    trainR = R;
    trainW = W;
    
    for x = 1:size(data,1)
        if indices(x) == n
            trainR(data(x,1),data(x,2)) = 0;
            trainW(data(x,1),data(x,2)) = 0;
        end
    end
    
    % Creating recommendation matrix %
    [U,V] = wnmfreg(trainR,trainW,100,1);
    predR = U*V;
    
    % Find top L movies for each user %
    for x = 1:users
        [val,ind] = sort(predR(x,:),'descend');
        topL(x,:) = ind(1,1:L);
    end
    
    % Classify test data and calculate precision %
    count = 0;
    total = 0;
    for x = 1:size(data,1)
        if indices(x) == n
            
            if W(data(x,1),data(x,2)) < 3.5
                Rating = 0;
            end
            
            if W(data(x,1),data(x,2)) >= 3.5
                Rating = 1;
            end
            
            if any(topL(data(x,1),:) == data(x,2))
                total = total + 1; 
                if Rating == 1
                    count = count + 1;
                end
            end
        end
    end
    
    if total ~= 0
        precision(a) = count/total;
        a = a+1;
    end
end

AvgPrec = mean(precision)