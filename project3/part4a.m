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

% Weighted NMF, ratings as weights, k = 10, 50, 100 %
[U10,V10] = wnmfrate(R,W,10);
[U50,V50] = wnmfrate(R,W,50);
[U100,V100] = wnmfrate(R,W,100);

% Construct prediction matrices %
UV10 = U10*V10;
UV50 = U50*V50;
UV100 = U100*V100;

% Calculate total MSE %
TLSE_WN_10 = 0;
TLSE_WN_50 = 0;
TLSE_WN_100 = 0;

for x = 1:size(data,1)
    TLSE_WN_10 = TLSE_WN_10 + data(x,3)*(1 - UV10(data(x,1),data(x,2)))^2;
    TLSE_WN_50 = TLSE_WN_50 + data(x,3)*(1 - UV50(data(x,1),data(x,2)))^2;
    TLSE_WN_100 = TLSE_WN_100 + data(x,3)*(1 - UV100(data(x,1),data(x,2)))^2;
end

TLSE_WN_10
TLSE_WN_50
TLSE_WN_100