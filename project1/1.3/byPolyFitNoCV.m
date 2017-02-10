% Read in data %
[data,text] = xlsread('LinRegData.xlsx');

% Fixed Training and Testing %
[train,test] = crossvalind('holdout', size(data,1), 0.1);
% randomly selects 10 percent of the data for testing
% train and test contain the indices for their respective data

% Separating observations and targets %
obs = data(:,1:size(data,2)-1);
target = data(:,7);

% Separating training and testing data %
c = 1;
for i = 1:size(data,1)
    if train(i,:)
        obsTrain(c,:) = obs(i,:);
        targetTrain(c,1) = target(i,1);
        c = c+1;
    end
end

d = 1;
for i = 1:size(data,1)
    if test(i,:)
        obsTest(d,:) = obs(i,:);
        targetTest(d,1) = target(i,1);
        d = d+1;
    end
end

% Warnings off %
warning('off');

% Fitting a polynomial to the data %
% For testing purposes, degree has been only run to 3
% You can set it to 10 (like our plots indicate) but it will take forever
% Tweak at your own peril!
for polydegree = 1:3 
    polymodel = polyfitn(obsTrain, targetTrain, polydegree);
    
    % Applying model to training, testing, and total data %
    targetTrainEst = polyvaln(polymodel, obsTrain);
    targetTestEst = polyvaln(polymodel, obsTest);
    targetTotalEst = polyvaln(polymodel, obs);
    
    % Calculating train RMSE, test RMSE, and total RMSE %
    trainMSE = immse(targetTrain,targetTrainEst);
    testMSE = immse(targetTest,targetTestEst);
    totalMSE = immse(targetTotalEst, target);
    
    trainRMSE(polydegree,1) = sqrt(trainMSE);
    testRMSE(polydegree,1) = sqrt(testMSE);
    totalRMSE(polydegree,1) = sqrt(totalMSE);
    
    clear polymodel targetTrainEst targetTestEst targetTotalEst 
end

trainRMSE
testRMSE
totalRMSE
