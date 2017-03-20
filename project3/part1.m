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

% Weighted NMF, k = 10, 50, 100 %
[U10,V10] = wnmfrule(R,10);
[U50,V50] = wnmfrule(R,50);
[U100,V100] = wnmfrule(R,100);

% Construct prediction matrices %
UV10 = U10*V10;
UV50 = U50*V50;
UV100 = U100*V100;

% Calculate total LSE %
TLSE10 = 0;
TLSE50 = 0;
TLSE100 = 0;

for x = 1:size(data,1)
    TLSE10 = TLSE10 + (data(x,3) - UV10(data(x,1),data(x,2)))^2;
    TLSE50 = TLSE50 + (data(x,3) - UV50(data(x,1),data(x,2)))^2;
    TLSE100 = TLSE100 + (data(x,3) - UV100(data(x,1),data(x,2)))^2;
end

TLSE10
TLSE50
TLSE100