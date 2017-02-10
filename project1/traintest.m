% Monday - Sunday has been mapped to the numbers 1 - 7 (Monday = 1, etc)
% work_flow_X has been mapped to number X+1 (work_flow_0 = 1, etc)
% File_XX has been mapped to number XX+1 (File_23 = 24, etc)

% Read in data %
[data,text] = xlsread('LinRegData.xlsx');

% 10 Fold Cross Validation %
indices = crossvalind('Kfold', size(data,1), 10);
% crossvalind randomly separates the data into 10 folds
% indices is a vector that contains the numbers 1 through 10
% the number indicates which fold that observation belongs to

% Separating observations and targets %
obs = data(:,1:size(data,2)-1);
target = data(:,7);

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
    
    % LS Regression %
    beta = obsTrain\targetTrain;
    
    % Calculating training data RMSE %
    targetTrainEst = obsTrain*beta; % our estimation of targetTrain
    trainMSE = immse(targetTrain,targetTrainEst); % MSE of the two
    trainRMSE(x,1) = sqrt(trainMSE); % RMSE for the xth test (training)
    
    % Calculating testing data RMSE %
    targetTestEst = obsTest*beta; % our estimation of targetTest
    testMSE = immse(targetTest,targetTestEst); % MSE of the two
    testRMSE(x,1) = sqrt(testMSE); % RMSE for the xth test (testing)
    
    % Calculating total data RMSE %
    targetTotalEst = obs*beta; % our estimation of target
    totalMSE = immse(target, targetTotalEst); % MSE of the two
    totalRMSE(x,1) = sqrt(totalMSE); % RMSE for the xth test (total)
    
    % Generate Fitted Values %
    fitval(:,x) = obs*beta;
    
    clear obsTrain targetTrain obsTest targetTest
end

% Calculate and display average RMSE values %
AvgTrainRMSE = sum(trainRMSE)/10;
AvgTestRMSE = sum(testRMSE)/10;
AvgTotalRMSE = sum(totalRMSE)/10;

AvgTrainRMSE
AvgTestRMSE
AvgTotalRMSE