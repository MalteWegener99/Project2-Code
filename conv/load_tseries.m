function pos = load_tseries(name)
fileID = fopen(name);
n = fread(fileID, 1,'uint64');
throw = fread(fileID, 1,'uint64');
pos = fread(fileID,[6,n],'6*float64',8);
pos = pos.';
fclose(fileID);
fileID = fopen(name);
n = fread(fileID, 1,'uint64');
times = fread(fileID,[1,n],'uint64',8*6);
times = times.';
pos = pos(1,1:3)
end