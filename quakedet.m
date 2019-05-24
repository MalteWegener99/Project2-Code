function quakes = quakedet()
load("data");
earthquakes = [];
for j = 2:length(data(1,:))
    testdata = data(:,j);
    isquake = ischange(testdata,'linear');
    for i = 1:length(isquake)
        if isquake(i) == 1
            earthquakes = [earthquakes;data(i-1,1)];
        end
    end
end
earthquakes = sort(earthquakes);
save('earthquakes.mat','earthquakes');
quakes = earthquakes;
end