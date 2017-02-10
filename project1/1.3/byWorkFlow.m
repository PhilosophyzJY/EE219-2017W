% Read in partitioned data by work flow %
[data,text] = xlsread('LinRegData.xlsx');
[wfzero,textzero] = xlsread('LinRegDataByWork.xlsx', 'w0');
[wfone,textone] = xlsread('LinRegDataByWork.xlsx', 'w1');
[wftwo,texttwo] = xlsread('LinRegDataByWork.xlsx', 'w2');
[wfthree,textthree] = xlsread('LinRegDataByWork.xlsx', 'w3');
[wffour,textfour] = xlsread('LinRegDataByWork.xlsx', 'w4');

% 10 Fold Cross Validation %
indiceszero = crossvalind('Kfold', size(wfzero,1), 10);
indicesone = crossvalind('Kfold', size(wfone,1), 10);
indicestwo = crossvalind('Kfold', size(wftwo,1), 10);
indicesthree = crossvalind('Kfold', size(wfthree,1), 10);
indicesfour = crossvalind('Kfold', size(wffour,1), 10);

% Separating observations and targets %
obs = data(:,1:size(data,2)-1);
target = data(:,7);

obszero = wfzero(:,1:size(wfzero,2)-1);
targetzero = wfzero(:,7);

obsone = wfone(:,1:size(wfone,2)-1);
targetone = wfone(:,7);

obstwo = wftwo(:,1:size(wftwo,2)-1);
targettwo = wftwo(:,7);

obsthree = wfthree(:,1:size(wfthree,2)-1);
targetthree = wfthree(:,7);

obsfour = wffour(:,1:size(wffour,2)-1);
targetfour = wffour(:,7);

% Generating RMSE values for 10 tests with 10 disjoint testing folds %
% Now, with 5 different work flows 0, 1, 2, 3, and 4 %
for x = 1:10
    
    % Generating training data %
    cZero = 1;
    cOne = 1;
    cTwo = 1;
    cThree = 1;
    cFour = 1;
    
    for i = 1:size(wfzero,1)
        if indiceszero(i,1) ~= x
            obsTrainZero(cZero,:) = obszero(i,:);
            targetTrainZero(cZero,1) = targetzero(i,1);
            cZero = cZero+1;
        end
    end
    
    for i = 1:size(wfone,1)
        if indicesone(i,1) ~= x
            obsTrainOne(cOne,:) = obsone(i,:);
            targetTrainOne(cOne,1) = targetone(i,1);
            cOne = cOne+1;
        end
    end
    
    for i = 1:size(wftwo,1)
        if indicestwo(i,1) ~= x
            obsTrainTwo(cTwo,:) = obstwo(i,:);
            targetTrainTwo(cTwo,1) = targettwo(i,1);
            cTwo = cTwo+1;
        end
    end
    
    for i = 1:size(wfthree,1)
        if indicesthree(i,1) ~= x
            obsTrainThree(cThree,:) = obsthree(i,:);
            targetTrainThree(cThree,1) = targetthree(i,1);
            cThree = cThree+1;
        end
    end
    
    for i = 1:size(wffour,1)
        if indicesfour(i,1) ~= x
            obsTrainFour(cFour,:) = obsfour(i,:);
            targetTrainFour(cFour,1) = targetfour(i,1);
            cFour = cFour+1;
        end
    end
    
    % Generating testing data %
    dZero = 1;
    dOne = 1;
    dTwo = 1;
    dThree = 1;
    dFour = 1;
    
    for i = 1:size(wfzero,1)
        if indiceszero(i,1) == x
            obsTestZero(dZero,:) = obszero(i,:);
            targetTestZero(dZero,1) = targetzero(i,1);
            dZero = dZero+1;
        end
    end
    
    for i = 1:size(wfone,1)
        if indicesone(i,1) == x
            obsTestOne(dOne,:) = obsone(i,:);
            targetTestOne(dOne,1) = targetone(i,1);
            dOne = dOne+1;
        end
    end
    
    for i = 1:size(wftwo,1)
        if indicestwo(i,1) == x
            obsTestTwo(dTwo,:) = obstwo(i,:);
            targetTestTwo(dTwo,1) = targettwo(i,1);
            dTwo = dTwo+1;
        end
    end
    
    for i = 1:size(wfthree,1)
        if indicesthree(i,1) == x
            obsTestThree(dThree,:) = obsthree(i,:);
            targetTestThree(dThree,1) = targetthree(i,1);
            dThree = dThree+1;
        end
    end
    
    for i = 1:size(wffour,1)
        if indicesfour(i,1) == x
            obsTestFour(dFour,:) = obsfour(i,:);
            targetTestFour(dFour,1) = targetfour(i,1);
            dFour = dFour+1;
        end
    end
    
    % LS Regression %
    betaZero = obsTrainZero\targetTrainZero;
    betaOne = obsTrainOne\targetTrainOne;
    betaTwo = obsTrainTwo\targetTrainTwo;
    betaThree = obsTrainThree\targetTrainThree;
    betaFour = obsTrainFour\targetTrainFour;
    
    % Calculating training data RMSE %
    targetTrainEstZero = obsTrainZero*betaZero;
    trainMSEZero = immse(targetTrainZero,targetTrainEstZero);
    
    targetTrainEstOne = obsTrainOne*betaOne;
    trainMSEOne = immse(targetTrainOne,targetTrainEstOne);
    
    targetTrainEstTwo = obsTrainTwo*betaTwo;
    trainMSETwo = immse(targetTrainTwo,targetTrainEstTwo);
    
    targetTrainEstThree = obsTrainThree*betaThree;
    trainMSEThree = immse(targetTrainThree,targetTrainEstThree);
    
    targetTrainEstFour = obsTrainFour*betaFour;
    trainMSEFour = immse(targetTrainFour,targetTrainEstFour);
    
    trainRMSE(x,1) = sqrt(trainMSEZero);
    trainRMSE(x,2) = sqrt(trainMSEOne);
    trainRMSE(x,3) = sqrt(trainMSETwo);
    trainRMSE(x,4) = sqrt(trainMSEThree);
    trainRMSE(x,5) = sqrt(trainMSEFour);
    
    % Calculating testing data RMSE %
    targetTestEstZero = obsTestZero*betaZero;
    testMSEZero = immse(targetTestZero,targetTestEstZero);
    
    targetTestEstOne = obsTestOne*betaOne;
    testMSEOne = immse(targetTestOne,targetTestEstOne);
    
    targetTestEstTwo = obsTestTwo*betaTwo;
    testMSETwo = immse(targetTestTwo,targetTestEstTwo);
    
    targetTestEstThree = obsTestThree*betaThree;
    testMSEThree = immse(targetTestThree,targetTestEstThree);
    
    targetTestEstFour = obsTestFour*betaFour;
    testMSEFour = immse(targetTestFour,targetTestEstFour);
    
    testRMSE(x,1) = sqrt(testMSEZero);
    testRMSE(x,2) = sqrt(testMSEOne);
    testRMSE(x,3) = sqrt(testMSETwo);
    testRMSE(x,4) = sqrt(testMSEThree);
    testRMSE(x,5) = sqrt(testMSEFour);
    
    % Calculating total data RMSE (WF) %
    targetTotalEstZero = obszero*betaZero;
    totalMSEZero = immse(targetzero,targetTotalEstZero);
    
    targetTotalEstOne = obsone*betaOne;
    totalMSEOne = immse(targetone,targetTotalEstOne);
    
    targetTotalEstTwo = obstwo*betaTwo;
    totalMSETwo = immse(targettwo,targetTotalEstTwo);
    
    targetTotalEstThree = obsthree*betaThree;
    totalMSEThree = immse(targetthree,targetTotalEstThree);
    
    targetTotalEstFour = obsfour*betaFour;
    totalMSEFour = immse(targetfour,targetTotalEstFour);
    
    totalRMSE_WF(x,1) = sqrt(totalMSEZero);
    totalRMSE_WF(x,2) = sqrt(totalMSEOne);
    totalRMSE_WF(x,3) = sqrt(totalMSETwo);
    totalRMSE_WF(x,4) = sqrt(totalMSEThree);
    totalRMSE_WF(x,5) = sqrt(totalMSEFour);
    
    % Calculating total data RMSE %
    for i = 1:size(data,1)
        switch data(i,4)
            case 1
                targetTotalEst(i,1) = obs(i,:)*betaZero;
            case 2
                targetTotalEst(i,1) = obs(i,:)*betaOne;
            case 3
                targetTotalEst(i,1) = obs(i,:)*betaTwo;
            case 4
                targetTotalEst(i,1) = obs(i,:)*betaThree;
            case 5
                targetTotalEst(i,1) = obs(i,:)*betaFour;
            otherwise
                disp('Error')
        end
    end
    
    totalMSE = immse(target, targetTotalEst); % MSE of the two
    totalRMSE(x,1) = sqrt(totalMSE); % RMSE for the xth test (total)
    
    if (x ~= 10)
        clear obsTrainZero targetTrainZero obsTestZero targetTestZero
        clear obsTrainOne targetTrainOne obsTestOne targetTestOne
        clear obsTrainTwo targetTrainTwo obsTestTwo targetTestTwo
        clear obsTrainThree targetTrainThree obsTestThree targetTestThree
        clear obsTrainFour targetTrainFour obsTestFour targetTestFour
    end
    
end

% Calculate and display average RMSE values %
AvgZeroTrainRMSE = sum(trainRMSE(:,1))/10;
AvgOneTrainRMSE = sum(trainRMSE(:,2))/10;
AvgTwoTrainRMSE = sum(trainRMSE(:,3))/10;
AvgThreeTrainRMSE = sum(trainRMSE(:,4))/10;
AvgFourTrainRMSE = sum(trainRMSE(:,5))/10;

AvgZeroTestRMSE = sum(testRMSE(:,1))/10;
AvgOneTestRMSE = sum(testRMSE(:,2))/10;
AvgTwoTestRMSE = sum(testRMSE(:,3))/10;
AvgThreeTestRMSE = sum(testRMSE(:,4))/10;
AvgFourTestRMSE = sum(testRMSE(:,5))/10;

AvgZeroTotalRMSE = sum(totalRMSE_WF(:,1))/10;
AvgOneTotalRMSE = sum(totalRMSE_WF(:,2))/10;
AvgTwoTotalRMSE = sum(totalRMSE_WF(:,3))/10;
AvgThreeTotalRMSE = sum(totalRMSE_WF(:,4))/10;
AvgFourTotalRMSE = sum(totalRMSE_WF(:,5))/10;

AvgTotalRMSE = sum(totalRMSE(:,1))/10;

AvgZeroTestRMSE
AvgOneTestRMSE
AvgTwoTestRMSE
AvgThreeTestRMSE
AvgFourTestRMSE 

AvgTotalRMSE