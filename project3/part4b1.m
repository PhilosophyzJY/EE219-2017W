% Change lambda as needed %
lambda = 0.01

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

% Weighted NMF, ratings as weights, k = 10, 50, 100, regularization %
[U10,V10] = wnmfreg(R,W,10,lambda);
[U50,V50] = wnmfreg(R,W,50,lambda);
[U100,V100] = wnmfreg(R,W,100,lambda);

% Construct prediction matrices %
UV10 = U10*V10;
UV50 = U50*V50;
UV100 = U100*V100;

% Calculate total LSE %
TLSE_WNR_10 = 0;
TLSE_WNR_50 = 0;
TLSE_WNR_100 = 0;

for x = 1:size(data,1)
    TLSE_WNR_10 = TLSE_WNR_10 + data(x,3)*(1 - UV10(data(x,1),data(x,2)))^2;
    TLSE_WNR_50 = TLSE_WNR_50 + data(x,3)*(1 - UV50(data(x,1),data(x,2)))^2;
    TLSE_WNR_100 = TLSE_WNR_100 + data(x,3)*(1 - UV100(data(x,1),data(x,2)))^2;
end

lambda
TLSE_WNR_10
TLSE_WNR_50
TLSE_WNR_100