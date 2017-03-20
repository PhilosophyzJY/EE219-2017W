% Read in data %
[data,text] = xlsread('RMF.xlsx');
users = max(data(:,1)); % number of users
movies = max(data(:,2)); % number of movies

% Initialization %
R = zeros(users,movies);
W = zeros(users,movies);

% Construct R 1-0 matrix and rating W matrix %
for x = 1:size(data,1)
    R(data(x,1),data(x,2)) = 1;
    W(data(x,1),data(x,2)) = data(x,3);
end

% Generate 10-Fold CV indices %
indices = crossvalind('Kfold',size(data,1), 10);

% Choose random fold for test movies %
n = round(rand*10);

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

% Hit rate and false alarm %
L = 1
p = 1;

while L < movies  
    % Find top L movies for each user %
    topL = zeros(users,L);
    
    for x = 1:users
        [val,ind] = sort(predR(x,:),'descend');
        topL(x,:) = ind(1,1:L);
    end
    
    counthr = 0;
    totalhr = 0;
    countfa = 0;
    totalfa = 0;
    
    for x = 1:size(data,1)
        if indices(x) == n
            
            if W(data(x,1),data(x,2)) < 3.5
                Rating = 0;
            end
            
            if W(data(x,1),data(x,2)) >= 3.5
                Rating = 1;
            end
            
            % hit rate %
            if Rating == 1
                totalhr = totalhr + 1;
                if any(topL(data(x,1),:) == data(x,2))
                    counthr = counthr + 1;
                end
            end
            
            % false alarm %
            if Rating == 0
                totalfa = totalfa + 1;
                if any(topL(data(x,1),:) == data(x,2))
                    countfa = countfa + 1;
                end
            end    
        end
    end
    
    hrfa(p,1) = countfa/totalfa;
    hrfa(p,2) = counthr/totalhr;
    p = p + 1;
    L = L + 500
end

xlswrite('Hit Rate vs False Alarm.xlsx',hrfa);
