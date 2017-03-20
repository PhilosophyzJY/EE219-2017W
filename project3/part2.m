% Read in data %
[data,text] = xlsread('RMF.xlsx');
users = max(data(:,1)); % number of users
movies = max(data(:,2)); % number of movies

% Initialization %
R = NaN(users,movies);

% Construct R matrix %
for x = 1:size(data,1)
    R(data(x,1),data(x,2)) = data(x,3);
end

% Generate 10-Fold CV indices %
indices = crossvalind('Kfold',size(data,1), 10);

% Predictions via 10-Fold CV %
AvgAbsError = zeros(10,1);

for n = 1:10
    % Setting nth fold data to NaN %
    trainR = R;
    for x = 1:size(data,1)
        if indices(x) == n
            trainR(data(x,1),data(x,2)) = NaN;
        end
    end
    
    % Creating recommendation matrix %
    [U,V] = wnmfrule(trainR,100);
    predR = U*V;
    
    % Calculate average absolute error %
    error = 0;
    for x = 1:size(data,1)
        if indices(x) == n
            error = error + abs(predR(data(x,1),data(x,2)) - R(data(x,1),data(x,2)));
        end
    end
    
    AvgAbsError(n,1) = error/sum(indices(:) == n,1);    
end

AvgAbsError
AvgTestError = mean(AvgAbsError)
MinAvgError = min(AvgAbsError)
MaxAvgError = max(AvgAbsError)