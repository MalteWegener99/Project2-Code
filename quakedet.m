function quakes = quakedet()
load("data");
earthquakes = [];
testdata = data(:,2);
isquake = ischange(testdata,'linear',1e-8);
for i = 1:length(isquake)
    if isquake(i) == 1
        earthquakes = [earthquakes;data(i,:)];
    end
end
save('earthquakes.mat','earthquakes');
quakes = earthquakes;
end