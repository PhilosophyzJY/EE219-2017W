% Read in data %
[data,text] = xlsread('LinRegData.xlsx');

% 10 Fold Cross Validation %
indices = crossvalind('Kfold', size(data,1), 10);

% Separating observations and targets %
obs = data(:,1:size(data,2)-1);
target = data(:,7);

% Warnings off %
warning('off');

% Fitting a polynomial to the data %
% For testing purposes, degree has been only run to 3
% You can set it to 10 (like our plots indicate) but it will take forever
% Tweak at your own peril!
for polydegree = 1:3
    
    % Generating RMSE values for 10 tests with 10 disjoint testing folds %
    for x = 1:10
        
        % Generating training data %
        c = 1;
        for i = 1:size(data,1)
            if indices(i,1) ~= x % ignore the xth fold for training data
                obsTrain(c,:) = obs(i,:);
                targetTrain(c,1) = target(i,1);
                c = c+1;
            end
        end
        
        % Generating testing data %
        d = 1;
        for i = 1:size(data,1)
            if indices(i,1) == x % include the xth fold for testing data
                obsTest(d,:) = obs(i,:);
                targetTest(d,1) = target(i,1);
                d = d+1;
            end
        end
        
        % Fitting Polynomial to training data %
        polymodel = polyfitn(obsTrain, targetTrain, polydegree);
        
        % Applying model to training, testing, and total data %
        targetTrainEst = polyvaln(polymodel, obsTrain);
        targetTestEst = polyvaln(polymodel, obsTest);
        targetTotalEst = polyvaln(polymodel, obs);
        
        % Calculating train RMSE, test RMSE, and total RMSE %
        trainMSE = immse(targetTrain,targetTrainEst);
        testMSE = immse(targetTest,targetTestEst);
        totalMSE = immse(targetTotalEst, target);
        
        trainRMSE(x,1) = sqrt(trainMSE);
        testRMSE(x,1) = sqrt(testMSE);
        totalRMSE(x,1) = sqrt(totalMSE);
        
        clear obsTrain targetTrain obsTest targetTest
        clear polymodel targetTrainEst targetTestEst targetTotalEst
    end
    
    AvgTrainRMSE(polydegree,1) = sum(trainRMSE)/10;
    AvgTestRMSE(polydegree,1) = sum(testRMSE)/10;
    AvgTotalRMSE(polydegree,1) = sum(totalRMSE)/10;
    
    clear trainRMSE testRMSE totalRMSE
end

AvgTrainRMSE
AvgTestRMSE
AvgTotalRMSE