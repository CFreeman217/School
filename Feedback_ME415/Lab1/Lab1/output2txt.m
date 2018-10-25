SF2 = table(time, input, output, voltage);
writetable(SF2)
SF2_data = table(data_th(:,1), data_th(:,3), data_vm(:,2));
writetable(SF2_data)