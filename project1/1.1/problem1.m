% Read in data %
[data,text] = xlsread('w0data.xlsx');

c0 = 1;
c1 = 1;
c2 = 1;
c3 = 1;
c4 = 1;
c5 = 1;

for n = 1:size(data,1)
    if strcmp(text(n+1,5), 'File_0')
        w(1,c0) = data(n,6);
        c0 = c0+1;
    end
    
    if strcmp(text(n+1,5), 'File_1')
        w(2,c1) = data(n,6);
        c1 = c1+1;
    end   
    
    if strcmp(text(n+1,5), 'File_2')
        w(3,c2) = data(n,6);
        c2 = c2+1;
    end
    
    if strcmp(text(n+1,5), 'File_3')
        w(4,c3) = data(n,6);
        c3 = c3+1;
    end   
                                            
    if strcmp(text(n+1,5), 'File_4')
        w(5,c4) = data(n,6);
        c4 = c4+1;
    end                        

    if strcmp(text(n+1,5), 'File_5')
        w(6,c5) = data(n,6);
        c5 = c5+1;
    end   
end

xlswrite('w0plot',w',1,'B2');
clear

c0 = 1;
c1 = 1;
c2 = 1;
c3 = 1;
c4 = 1;
c5 = 1;

for n = 1:size(data,1)
    if strcmp(text(n+1,5), 'File_6')
        w(1,c0) = data(n,6);
        c0 = c0+1;
    end
    
    if strcmp(text(n+1,5), 'File_7')
        w(2,c1) = data(n,6);
        c1 = c1+1;
    end   
    
    if strcmp(text(n+1,5), 'File_8')
        w(3,c2) = data(n,6);
        c2 = c2+1;
    end
    
    if strcmp(text(n+1,5), 'File_9')
        w(4,c3) = data(n,6);
        c3 = c3+1;
    end   
                                            
    if strcmp(text(n+1,5), 'File_10')
        w(5,c4) = data(n,6);
        c4 = c4+1;
    end                        

    if strcmp(text(n+1,5), 'File_11')
        w(6,c5) = data(n,6);
        c5 = c5+1;
    end   
end

xlswrite('w1plot',w',1,'B2');
clear

c0 = 1;
c1 = 1;
c2 = 1;
c3 = 1;
c4 = 1;
c5 = 1;

for n = 1:size(data,1)
    if strcmp(text(n+1,5), 'File_12')
        w(1,c0) = data(n,6);
        c0 = c0+1;
    end
    
    if strcmp(text(n+1,5), 'File_13')
        w(2,c1) = data(n,6);
        c1 = c1+1;
    end   
    
    if strcmp(text(n+1,5), 'File_14')
        w(3,c2) = data(n,6);
        c2 = c2+1;
    end
    
    if strcmp(text(n+1,5), 'File_15')
        w(4,c3) = data(n,6);
        c3 = c3+1;
    end   
                                            
    if strcmp(text(n+1,5), 'File_16')
        w(5,c4) = data(n,6);
        c4 = c4+1;
    end                        

    if strcmp(text(n+1,5), 'File_17')
        w(6,c5) = data(n,6);
        c5 = c5+1;
    end   
end

xlswrite('w2plot',w',1,'B2');
clear

c0 = 1;
c1 = 1;
c2 = 1;
c3 = 1;
c4 = 1;
c5 = 1;

for n = 1:size(data,1)
    if strcmp(text(n+1,5), 'File_18')
        w(1,c0) = data(n,6);
        c0 = c0+1;
    end
    
    if strcmp(text(n+1,5), 'File_19')
        w(2,c1) = data(n,6);
        c1 = c1+1;
    end   
    
    if strcmp(text(n+1,5), 'File_20')
        w(3,c2) = data(n,6);
        c2 = c2+1;
    end
    
    if strcmp(text(n+1,5), 'File_21')
        w(4,c3) = data(n,6);
        c3 = c3+1;
    end   
                                            
    if strcmp(text(n+1,5), 'File_22')
        w(5,c4) = data(n,6);
        c4 = c4+1;
    end                        

    if strcmp(text(n+1,5), 'File_23')
        w(6,c5) = data(n,6);
        c5 = c5+1;
    end   
end

xlswrite('w3plot',w',1,'B2');
clear

c0 = 1;
c1 = 1;
c2 = 1;
c3 = 1;
c4 = 1;
c5 = 1;

for n = 1:size(data,1)
    if strcmp(text(n+1,5), 'File_24')
        w(1,c0) = data(n,6);
        c0 = c0+1;
    end
    
    if strcmp(text(n+1,5), 'File_25')
        w(2,c1) = data(n,6);
        c1 = c1+1;
    end   
    
    if strcmp(text(n+1,5), 'File_26')
        w(3,c2) = data(n,6);
        c2 = c2+1;
    end
    
    if strcmp(text(n+1,5), 'File_27')
        w(4,c3) = data(n,6);
        c3 = c3+1;
    end   
                                            
    if strcmp(text(n+1,5), 'File_28')
        w(5,c4) = data(n,6);
        c4 = c4+1;
    end                        

    if strcmp(text(n+1,5), 'File_29')
        w(6,c5) = data(n,6);
        c5 = c5+1;
    end   
end

xlswrite('w4plot',w',1,'B2');
clear
