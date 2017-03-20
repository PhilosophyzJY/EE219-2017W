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

% ROC via 10-Fold CV %
z = 1;
thold = 0.5
while thold <= 4.5
    p = 1;
    
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
        
        % Thresholding %
        c = 1;
        
        for x = 1:size(data,1)
            if indices(x) == n
                if predR(data(x,1),data(x,2)) < thold
                    Classifier(c,1) = 0;
                end
                
                if predR(data(x,1),data(x,2)) >= thold
                    Classifier(c,1) = 1;
                end
                
                if R(data(x,1),data(x,2)) < 3.5
                    Classifier(c,2) = 0;
                end
                
                if R(data(x,1),data(x,2)) >= 3.5
                    Classifier(c,2) = 1;
                end
                
                c = c + 1;
            end
        end
        
        if sum(Classifier(:,1) == 1) == 0
            continue;
        end
        
        % Calculating precision and recall %
        match = 0;
        
        for x = 1:size(Classifier,1)
            if Classifier(x,1) == 1 && Classifier(x,2) == 1
                match = match + 1;
            end
        end
        
        prec(p,1) = match / sum(Classifier(:,1) == 1);
        
        match = 0;
        
        for x = 1:size(Classifier,1)
            if Classifier(x,2) == 1 && Classifier(x,1) == 1
                match = match + 1;
            end
        end
        
        rec(p,1) = match / sum(Classifier(:,2) == 1);
        p = p + 1;
        
        clear Classifier
    end
    
    precision(z,1) = mean(prec);
    recall(z,1) = mean(rec);
    z = z + 1;
    thold = thold + 0.5
    clear prec rec
end

curve(:,1) = recall;
curve(:,2) = precision;
xlswrite('ROC Curve.xlsx',curve);