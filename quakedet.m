function quakes = quakedet(data)
testdata = data(:,start);
isquake = ischange(testdata);
for i = 1:length(isquake)
    if isquake(i,1) == 1
    end
end