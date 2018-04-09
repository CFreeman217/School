
def hydroCarbonMolMass(num_carbon):
	num_hydrogen = ( num_carbon * 2 ) + 2
	hyd_wgt = 1.008
	car_wgt = 12.011
	tot_mass = (num_carbon * car_wgt) + (num_hydrogen * hyd_wgt)
	ret_str = "C" + str(num_carbon) + "  H" + str(num_hydrogen) + "  Molar Mass =  " + str(tot_mass) + " kg/kmol"
	print(ret_str)
	
	

for x in range(19):
	hydroCarbonMolMass(x)

user_carbon = int(input("Number of carbons in saturated hydrocarbon chain: "))

hydroCarbonMolMass(user_carbon)