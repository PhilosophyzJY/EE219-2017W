% Read in data %
[data,text] = xlsread('LinRegData.xlsx'); % read in data
obs = data(:,1:size(data,2)-1); % observations 
target = data(:,7); % targets

% Transpose data to fit function parameter sizes %
obs = obs';
target = target';

% Generate the function-fitting neural network %
hiddenLayerSize = 75; % how many hidden layers
trainFX = 'trainlm'; % what type of function
net = fitnet(hiddenLayerSize, trainFX); % create network

% 10 Fold Cross Validation %
net.divideParam.trainRatio = 90/100; % 90% of observations to train
net.divideParam.testRatio = 10/100; % 10% of observations to test

% Train the network with the data %
[net,tr] = train(net, obs, target);

% View the Model %
view(net);

% Output the fitted (estimated) values and calculate the RMSE %
targetEst = net(obs); 
MSE = immse(target,targetEst);
RMSE = sqrt(MSE); 

% Display RMSE %
RMSE
