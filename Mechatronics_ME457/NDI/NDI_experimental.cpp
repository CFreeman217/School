/*
44 - variable declaration
95 - accel/gyro vars
409 - log file text header
483 - student loop section
528 - log file data
590 - console output
ME457_Quad3
cd Navio2/C++/Examples/NewCodeQuad

*/

// custom function includes
#include "Navio/ScaleVars.h" // functions for re-scaling a value within a specified output range
// log file includes
#include <fstream>
#include <string>
// standard includes
#include <cstdlib>
#include <sys/time.h>
#include <unistd.h>
#include <iostream>
#include <tuple>
#include <iomanip> // used to force GPS data to output with correct precision
// Navio2 includes
// barometer includes
#include "Navio/MS5611.h"
#include <cmath>
// RC Input includes
#include <Navio/RCInput.h>
// IMU Includes
#include "Navio/MPU9250.h"
#include "Navio/LSM9DS1.h"
// PWM Output Includes
#include "Navio/PWM.h"
#include "Navio/Util.h"
// AHRS Includes
#include "AHRS2.hpp"
// ADC Includes
#include <Navio/ADC.h>
#include "Navio/digital_filter.h"
#include "Navio/buffer.h"

using namespace std;
//----------------------------------------------------------------------------------------------------------Saturation Parameters
#define MAX_DUTY_CYCLE 0.6
#define NEUTRAL 1.5

//------------------------------------------------------------------------------------------------------------Filter Declarations
// Assign motors to Navio output pins
#define M1 0
#define M2 1
#define M3 2
#define M4 3

// Throttle command storage
float throttle_cmd;
// Initialize variables for pitch, roll, and yaw DESIRED and MEASURED
float pitch_d = 0, roll_d = 0, yaw_d = 0;
float pitch_m = 0, roll_m = 0, yaw_m = 0;
// Variables to store PID errors for pitch, roll, and yaw
float err_pp = 0, err_pi = 0, err_pd = 0;
float err_rp = 0, err_ri = 0, err_rd = 0;
float err_yp = 0, err_yi = 0, err_yd = 0;
// Store error from previous iteration
float err_p_old = 0, err_r_old = 0, err_y_old = 0;
// Variables to store calculated motor commands
float pit_lam = 0, rol_lam = 0, yaw_lam = 0;
// Initialize motor commands
float M1cmd = 0, M2cmd = 0, M3cmd = 0, M4cmd = 0;
// PID Gains for pitch and roll
float k_p = 38e-4;
float k_i = 0;
float k_d = 73e-5;

// PID Gains for yaw
float k_py = .26;
float k_iy = .0032;
float k_dy = 0.00;

// Nonlinear Dynamic Inversion Experiment

#define OLS_PTS 25
float mem_pts[9][OLS_PTS]; // pitch_cmd, roll_cmd, yaw_cmd, pitch_meas, roll_meas, yaw_meas, pit_dot, rol_dot, yaw_dot
float pm_old = 0.1, rm_old = 0.1, ym_old = 0.1; // collect old state measurements for derivative

std::tuple<double, double, double, double, double, double, double, double, double> OLS_2var (float in_pts[9][OLS_PTS])
{
	// 1 = pitch , 2 = roll , 3 = yaw
	float sx1, sx2, sx3; // commands
	float sy1, sy2, sy3; // measurements
	float sz1, sz2, sz3; // rates
	float sxy1, sxy2, sxy3;
	float sxz1, sxz2, sxz3;
	float syz1, syz2, syz3;
	float mx1, mx2, mx3;
	float my1, my2, my3;
	float mz1, mz2, mz3;
	float s2x1, s2x2, s2x3;
	float s2y1, s2y2, s2y3;
	float s2z1, s2z2, s2z3;
	float coef_a1, coef_a2, coef_a3;
	float coef_b1, coef_b2, coef_b3;
	float coef_c1, coef_c2, coef_c3;

	for(int i = 0, i < OLS_PTS, i++)
	{
		sx1 += in_pts[0][i];
		sx2 += in_pts[1][i];
		sx3 += in_pts[2][i];
		sy1 += in_pts[3][i];
		sy2 += in_pts[4][i];
		sy3 += in_pts[5][i];
		sz1 += in_pts[6][i];
		sz2 += in_pts[7][i];
		sz3 += in_pts[8][i];
		sxy1 += in_pts[0][i] * in_pts[3][i];
		sxz1 += in_pts[0][i] * in_pts[6][i];
		syz1 += in_pts[3][i] * in_pts[6][i];
		sxy2 += in_pts[1][i] * in_pts[4][i];
		sxz2 += in_pts[1][i] * in_pts[7][i];
		syz2 += in_pts[4][i] * in_pts[7][i];
		sxy3 += in_pts[2][i] * in_pts[5][i];
		sxz3 += in_pts[2][i] * in_pts[8][i];
		syz3 += in_pts[5][i] * in_pts[8][i];
	}
	sxy1 -= (sx1*sy1)/OLS_PTS;
	sxz1 -= (sx1*sz1)/OLS_PTS;
	syz1 -= (sy1*sz1)/OLS_PTS;
	sxy2 -= (sx2*sy2)/OLS_PTS;
	sxz2 -= (sx2*sz2)/OLS_PTS;
	syz2 -= (sy2*sz2)/OLS_PTS;
	sxy3 -= (sx3*sy3)/OLS_PTS;
	sxz3 -= (sx3*sz3)/OLS_PTS;
	syz3 -= (sy3*sz3)/OLS_PTS;
	mx1 = sx1/OLS_PTS;
	mx2 = sx2/OLS_PTS;
	mx3 = sx3/OLS_PTS;
	my1 = sy1/OLS_PTS;
	my2 = sy2/OLS_PTS;
	my3 = sy3/OLS_PTS;
	mz1 = sz1/OLS_PTS;
	mz2 = sz2/OLS_PTS;
	mz3 = sz3/OLS_PTS;
	for(int i = 0, i < OLS_PTS, i++)
	{
		s2x1 += pow(in_pts[0][i]-mx1,2);
		s2x2 += pow(in_pts[1][i]-mx2,2);
		s2x3 += pow(in_pts[2][i]-mx3,2);
		s2y1 += pow(in_pts[3][i]-my1,2);
		s2y2 += pow(in_pts[4][i]-my2,2);
		s2y3 += pow(in_pts[5][i]-my3,2);
		s2z1 += pow(in_pts[6][i]-mz1,2);
		s2z2 += pow(in_pts[7][i]-mz2,2);
		s2z3 += pow(in_pts[8][i]-mz3,2);
	}
	coef_b1 = (s2z1 * sxy1 - syz1 * sxz1) / (s2y1 * s2z1 - pow(syz1,2));
	coef_c1 = (s2y1 * sxz1 - syz1 * sxy1) / (s2y1 * s2z1 - pow(syz1,2));
	coef_a1 = mx1 - coef_b1*my1 - coef_c1*mz1;
	coef_b2 = (s2z2 * sxy2 - syz2 * sxz2) / (s2y2 * s2z2 - pow(syz2,2));
	coef_c2 = (s2y2 * sxz2 - syz2 * sxy2) / (s2y2 * s2z2 - pow(syz2,2));
	coef_a2 = mx2 - coef_b2*my2 - coef_c2*mz2;
	coef_b3 = (s2z3 * sxy3 - syz3 * sxz3) / (s2y3 * s2z3 - pow(syz3,2));
	coef_c3 = (s2y3 * sxz3 - syz3 * sxy3) / (s2y3 * s2z3 - pow(syz3,2));
	coef_a3 = mx3 - coef_b3*my3 - coef_c3*mz3;
	return std::make_tuple(coef_a1, coef_b1, coef_c1, coef_a2, coef_b2, coef_c2, coef_a3, coef_b3, coef_c3);
}



// float zeta = 1; // Used in control law feedback
// float k_torque = 1; // Constant to convert PWM to torque
// float k_2 = .05; // Response time of the error, smaller = slower
// float k_1 = pow(k_2, 0.5)*2*zeta; // other crap
// float I_mom = 12; // Moment of Inertia about center of mass
// float b_damp = 0.01; // damping coefficient for rotor blades

// float p_dot = 0, r_dot = 0, y_dot = 0;
// float p_old = 0, r_old = 0, y_old = 0;

// Zeigler-Nichols Calculated Gains from Tangent Method:
// float k_py = 0.20135228677379483;
// float k_iy = 0.24889034211841138;
// float k_dy = 0.0407235;
//
// Butterworth filter initialization:
// const int order = 2;
// const char low = 'l'; // for low pass
// const char high = 'h';
// const float fc = 1; // Hz
// const float fs = 100; // Hz

// digital_filter yaw_filt(order,low,fc,fs); // in order to use the custom filter class we have to declare an instance of the type

//---------------------------------------------------------------------------------------------------User Configurable Parameters
const bool dbmsg_global = false; // set flag to display all debug messages
bool dbmsg_local  = false; // change in the code at a specific location to view local messages only
char control_type = 'x'; // valid options:  p=PID , n=NDI , g=glide (no spin), m=multisine , s=input sweep, c=rc control
char heading_type = 'd'; // valid otpoins 1=N, 2=E, 3=S, 4=W, u=user, c=rc control, n=navigation algorithm, d=dumb navigation
float user_heading = 115; //degress, only used if us is the heading type
bool live_gains = false;


//-------------------------------------------------------------------------------------------Loop timing (scheduler) Declarations
#define NUM_LOOPS  9
bool main_loop_active = true; // will bind this to an RC channel later for online tuning
struct timeval time_obj;
unsigned long long tse; // time since epoch (us)
unsigned long long time_start; // time from the beginning of current program executing (us)
unsigned long long time_now; // current time since the program starting executing (us)

//---------------------------------------------------------------------------------------------------------Barometer Declarations
int baro_step = 0; // declare the step counter (used to delay time from read to caclulate)
MS5611 barometer; // declare a new barometer object

// using the barometric equation in region 1 (valid for elevations up to 36,000ft)
// see wikipedia.org/wiki/Barometric_formula for more information
// using imperial units (some values use strange mixed units, Kelvin with imperial length?), has been tested and output looks ok
// CONSTANTS
const float Pb =  29.92126;    // static reference pressure for barometric equation (inHg)
const float Tb = 288.815;      // reference temperature for barometric equation (K) !!!not currently using this in the calculation
const float Lb =   -.0019812;  // standard temperature lapse rate (K/ft)
const float hb =   0.0;        // refernce height (ft), could be omitted but kept for generality
const float  R =   8.9494596e4;// universal gas constant (lbft^2)/(lbmolKs^2)
const float g0 =  32.17405;    // acceleration due to earth's gravity near the surface (ft/s^2)
const float  M =  28.9644;     // molar mass of earth's air (lb/lbmol)
// VARIABLES
float Tc  = 0.0; // temperature (C) <--read directly from sensor
float Tf  = 0.0; // temperature (F) <--this is not used for any calcs
float Tk  = 0.0; // temperature (K) <--converted for use in barometric equation
float Pm  = 0.0; // pressure (mbar) <--read directly from sensor
float Phg = 0.0; // pressure (inHg) <--converted for use in barometric equation
float msl = 0.0; // mean sea level altitude (ft) [should be close to 920ft for UMKC Flarsheim]

//----------------------------------------------------------------------------------------------------------RC Input Declarations
RCInput rcinput{}; const float input_range[2] = {1088,1940}; // range is the same for all channels
// for PID tuning
// const float output_range[6][2] ={{45,-45},{45,-45},{.9,1.9},{1,-1},{-.5,.5},{-.5,.5}};
const float output_range[6][2] = {{-25,25},{25,-25},{.9,1.7},{1,-1},{-.5,.5},{-.5,.5}};
float coefficients[6][2];

//---------------------------------------------------------------------------------------------------------------IMU Declarations
#define DECLINATION 1.70 //magnetic declination for KC
#define WRAP_THRESHOLD 160.00 // wrap threshold for wrap counter (yaw is +/-180, need to make it continuous
// vars to hold mpu values
float a_mpu[3] , a_mpu_ahrs[3];
float g_mpu[3] , g_mpu_ahrs[3];
float m_mpu[3] ;

//-------------------------------------------------------------------------------------------------------------Servo Declarations

//--------------------------------------------------------------------------------------------------------------AHRS Declarations
#define PI 3.14159
#define G_SI 9.81
AHRS ahrs_mpu_madgwick; // create a new object of type AHRS for the Madgwick filter
float roll_mpu_madgwick = 0 , pitch_mpu_madgwick = 0 , yaw_mpu_madgwick = 0; // euler angles for mpu madgwick
float offset_mpu[3];
float dt, maxdt;
float mindt = 0.01;
float dtsumm = 0;
int isFirst = 1;

//Campus Quad Offsets
float mag_offset_mpu[3] = {19.236,7.985,59.101};
float mag_rotation_mpu[3][3] = {{.769,-.166,.063},{-.166,.725,.075},{.063,.075,.976}};
float mag_offset_lsm[3] = {-5.388,1.707,72.647};
float mag_rotation_lsm[3][3] = {{.843,-.192,.088},{-.192,.677,.112},{.088,.112,.949}};

//-----------------------------------------------------------------------------------------------------------Logfile Declarations
// these are used to format the filename string
#define FILENAME_LENGTH 12
#define FILENAME_OFFSET 4
// leave extra room for '.csv' and potential '-1', '-2', etc.
char filename[FILENAME_LENGTH+6];
// log file location (relative path)
string file_location = "/home/pi/Navio2/C++/Examples/NewCodeQuad/LogFiles/";
// function to check if file exists so that the filename can be dynamically changed
bool file_exists(string name_of_file){
	ifstream checkfile(name_of_file); // try to read from the file
	return bool(checkfile);} // cast the result to bool, if file opens, this returns true (it exists)

int main( int argc , char *argv[])
{
	//----------------------------------------------------------------------------------------------------------------File Title Prefix
	int multisine_counter = 0;
	int parameter; // parameter is the argument passed in with the program call, create it here
	char *logfile_prefix; // pointer to a character array which will contain the log_file prefix when using the -d parameter
	string logfile_prefix_string; // previous variable will be converted to a string before using it to make a file
	logfile_prefix_string = file_location; // used to store the path
	string logfile_prefix_fromfile; // used to store the prefix when using the -f parameter
	ifstream ifs; // create a new file stream object, this will be reused for each file we need to read
	while((parameter = getopt(argc,argv, "hfd:")) != -1){ // read in the program options
		switch(parameter){ // switch on the character after the dash example:  sudo ./NewCode -d <filename>"
			case 'h' : // h parameter calls the help message
				cout << "Use option \"-d <FilePrefix>\" to insert a prefix into the filename" << endl;
				cout << "Use option \"-f\" to read configuration from file (configuration.csv)" << endl;
				return EXIT_FAILURE; // do not continue executing after displaying the help message
				break;
			case 'f' : // f parameter reads important variables from a configutation.txt file
				cout << "Reading user configuration from file" << endl;
				ifs.open("configuration.txt"); // open the configuration file
				ifs >> control_type; // read in the control type (character)
				cout << "Control type: " << control_type << endl; // echo to console
				ifs >> heading_type; // read in the heading type (character)
				cout << "Heading type: " << heading_type << endl; // echo to console
				ifs >> user_heading; // read in the heading (number), only used for user heading
				cout << "User heading: " << user_heading << " degrees" << endl; // echo to the console
				getline(ifs,logfile_prefix_fromfile); // this is a hack to get to the next line
				getline(ifs,logfile_prefix_fromfile); // read in the prefix from the configuration file
				logfile_prefix_string = file_location+logfile_prefix_fromfile+'_'; // stick an underscore after the file prefix
				cout << "Logfile prefix: " << logfile_prefix_fromfile << endl; // echo to the console
				ifs.close(); // close the file
				break;
			// this option reads in a prefix from the program call and uses the defaults for everything else
			case 'd' : logfile_prefix = optarg; logfile_prefix_string = file_location+string(logfile_prefix)+'_'; break;
			// stop execution if option flag is invalid
			case '?' : cout << "Invalid option.  Use -h for help" << endl; return EXIT_FAILURE;}}


	cout << endl;
	cout << "=======================================" << endl;
	cout << "         Begin Initialization          " << endl;
	cout << "=======================================" << endl;
	cout << endl;
	cout << "Reading mag calibration from file......" << endl;
	ifs.open ("/home/pi/Navio2/C++/Examples/NewCodeQuad/mpu_mag_cal.csv"); // name of the mpu mag calibration file
	if(ifs){ // if successful, read the values and print a message
		cout << "MPU9250 offsets:" << endl;
	for(int i = 0 ; i < 3 ; i++ ){ // colum iterator, offsets are the first row (1x3) inside the 4x3 data file
		if(i != 0){ // on the first and last iteration there is no comma to catch
			cout << ", "; // print a comma to make output readable
			char delim; // create a character inside this scope, it is just a dummy variable
			ifs >> delim;} // stream the comma to the dummy character so it can be discarded
		ifs >> mag_offset_mpu[i]; // stream the offsets into the correct position in the offset array
		cout << mag_offset_mpu[i];} // output the offset array to the console
	cout << endl; // end line, prepare to read/write the rotation matrix
	cout << "MPU9250 rotation matrix:" << endl;
	for(int i = 0 ; i < 3 ; i++ ){ // row iterator, matrix is 3x3
		for(int j = 0 ; j < 3 ; j++ ){ // column iterator
			if(j != 0){ // on the first and last iteration there is no comma to catch
				cout << ", "; // print a comma to make the output readable
				char delim; // create a character inside this scope, it is just a dummy variable
				ifs >> delim;} // stream the comma to the dummy character so it can be discarded
			ifs >> mag_rotation_mpu[i][j]; // stream the rotation matrix values to the correct positions in the array
			cout << mag_rotation_mpu[i][j];} // output the rotation matrix to the console
		cout << endl;}}
	else{ // if the file open operation is not successful
	cout << "Cannot read MPU offsets, using defaults" << endl;} // print that the file could not be read, this is not a fatal error
	ifs.close(); // close the current file to prepare for the next file read operation

	//-------------------------------------------------------------------------------------------Loop timing (scheduler) Initialization
	// initialize the time variables
	gettimeofday(&time_obj, NULL); // standard unix function to get the current time since epoch
	tse          = time_obj.tv_sec*1000000LL + time_obj.tv_usec; // time since epoch (converted to microseconds)
	time_start = tse; // time since epoch (ms), will be used to calculate time since start (beginning at 0us)

	// declare the scheduler frequencies
	cout << endl;
	cout << "Establishing loop frequencies.........." << endl;
	// 8-4-2017 changed all timer related variables to long long, timer variable (int) was overflowing and causing erratic timing
	// if code had been running for ~35 minutes, tested after fixing and overflow is no longer occuring after 35 minutes
	const float frequency [NUM_LOOPS] = {300,1000,1,100,50,20,10,.33,1}; //Hz
	unsigned long long duration [NUM_LOOPS]; // stores the expected time since last execution for a given loop
	unsigned long long timer [NUM_LOOPS]; // stores the time since the last execution in a given loop
	unsigned long long watcher [NUM_LOOPS]; // used for monitoring actual timer loop durations

	// calculate the scheduler us delay durations and populate the timer array with zeros
	cout << "Calculating loop delay durations......." << endl;
	cout << "Populating loop timers................." << endl;
	for(int i = 0 ; i < NUM_LOOPS ; i++){ // populate the durations using the passed values for frequency, echo everything to the console
		duration[i] = 1000000/frequency[i];
		if(dbmsg_global || dbmsg_local){cout << "Frequency is " << frequency[i] << "(Hz), duration is " << duration[i] << "(us)"<< endl;}
		timer[i] = 0;
		if(dbmsg_global || dbmsg_local){cout << "Timer is set to " << timer[i] << "(us), should all be zero" << endl;}
		watcher[i] = 0;}
	//---------------------------------------------------------------------------------------------------------Barometer Initialization
	cout << "Initializing barometer................." << endl;
	barometer.initialize();
	cout << " --Barometer successfully initalized-- " << endl;
	//----------------------------------------------------------------------------------------------------------RC Input Initialization
	cout << "Initilizing RC Input..................." << endl;
	rcinput.init();
	int rc_array [rcinput.channel_count]; // array for holding the values which are read from the controller
	float rc_array_scaled [rcinput.channel_count]; // array for holding the scaled values
	for(int i = 0 ; i < rcinput.channel_count ; i++ ){
		rc_array[i] = rcinput.read(i);} // read in each value using the private class function (converts to int automatically)
	cout << "Currently using " << rcinput.channel_count << " channels............." << endl;
	cout << " --RC Input successfully initialized-- " << endl;
	cout << "Creating RC Input range coefficients   " << endl;
	for(int i = 0 ; i < rcinput.channel_count ; i++){ // using a custom class for converting bounded values to values in a new range
		// in the Python version of this function, both parameters are returned by one function
		// since multiple values may not be returned by a single function this version uses a function for each scaling parameter
		coefficients[i][0] = calculate_slope(input_range,output_range[i]); // first call the slope calculator
		coefficients[i][1] = calculate_intercept(input_range,output_range[i],coefficients[i][0]); // next calculate the intercept
	}
	cout << "Successfully created range coefficients" << endl;

	//---------------------------------------------------------------------------------------------------------------IMU Initialization
	cout << "Initializing IMUs......................" << endl;
	InertialSensor *mpu;
	mpu = new MPU9250();
	mpu->initialize();
	cout << " --MPU9250 successfully initialized--" << endl;
	InertialSensor *lsm;
	cout << "Populating IMU sensor arrays..........." << endl;
	for(int i = 0; i < 3 ; i++){ // seed everything with a value of 0
		a_mpu[i]=g_mpu[i]=m_mpu[i] = 0.0;}
	//-------------------------------------------------------------------------------------------------------------Servo Initialization
	cout << "Initializing PWM Output................" << endl;
	PWM pwm_out;
	//create pwm output object and initialize right and left winch servos, stop execution if servos cannot be initialized
	// NOTE!!! if the code is erroring out here, the first thing to check is to make sure that you are are running the code with sudo
	if(!pwm_out.init(M1)){ // Motor 1
		cout << "Cannot Initialize Motor 1" << endl;
		cout << "Make sure you are root" << endl;
		return EXIT_FAILURE;}
	if(!pwm_out.init(M2)){ // Motor 2
		cout << "Cannot Initialize Motor 2" << endl;
		cout << "Make sure you are root" << endl;
		return EXIT_FAILURE;}
	if(!pwm_out.init(M3)){ // Motor 3
		cout << "Cannot Initialize Motor 3" << endl;
		cout << "Make sure you are root" << endl;
		return EXIT_FAILURE;}
	if(!pwm_out.init(M4)){ // Motor 4
		cout << "Cannot Initialize Motor 4" << endl;
		cout << "Make sure you are root" << endl;
		return EXIT_FAILURE;}
	cout << "Enabling PWM output channels..........." << endl;
	pwm_out.enable(M1); // both init() and enable() must be called to use the PWM output on a particular pin
	pwm_out.enable(M2); // both init() and enable() must be called to use the PWM output on a particular pin
	pwm_out.enable(M3); // both init() and enable() must be called to use the PWM output on a particular pin
	pwm_out.enable(M4); // both init() and enable() must be called to use the PWM output on a particular pin
	cout << "Setting PWM period for 50Hz............" << endl;
	pwm_out.set_period(M1 , 50); // set the PWM frequency to 50Hz
	pwm_out.set_period(M2 , 50); // set the PWM frequency to 50Hz
	pwm_out.set_period(M3 , 50); // set the PWM frequency to 50Hz
	pwm_out.set_period(M4 , 50); // set the PWM frequency to 50Hz

	cout << "  --PWM Output successfully enabled-- " << endl;

	// This is the ESC Calibration, problems with ESC can sometimes be fixed by make the value in usleep larger (longer delay)
	pwm_out.set_duty_cycle(M1, 1);
	pwm_out.set_duty_cycle(M2, 1);
	pwm_out.set_duty_cycle(M3, 1);
	pwm_out.set_duty_cycle(M4, 1);
	usleep(200000);
	pwm_out.set_duty_cycle(M1, 2);
	pwm_out.set_duty_cycle(M2, 2);
	pwm_out.set_duty_cycle(M3, 2);
	pwm_out.set_duty_cycle(M4, 2);
	usleep(200000);
	pwm_out.set_duty_cycle(M1, 1);
	pwm_out.set_duty_cycle(M2, 1);
	pwm_out.set_duty_cycle(M3, 1);
	pwm_out.set_duty_cycle(M4, 1);

	//--------------------------------------------------------------------------------------------------------------ADC Initialization
	cout << "Initializing ADC......................." << endl;
	ADC adc{};
	adc.init();
	float adc_array[adc.get_channel_count()] = {0.0f};
	for(int i = 0 ; i < ARRAY_SIZE(adc_array) ; i++){
		adc_array[i] = adc.read(i);}
	cout << "     --ADC successfully enabled--     " << endl;

	//-------------------------------------------------------------------------------------------------------------AHRS Initialization
	cout << "Initializing gyroscope................." << endl;
	cout << "Reading gyroscope offsets.............." << endl;
	// gyroscope offsets generated by sampling the gyroscope 100 times when the program executes, averaging the 100 samples
	// and then subtracting off the newly acquired offset values evertime the gyro is read later on in the code
	for(int i = 0 ; i < 100 ; i++){
		// read both sensors, we are only concerned with gyroscope information right now
		mpu->update(); // update the mpu sensor
		mpu->read_gyroscope(&g_mpu[0],&g_mpu[1],&g_mpu[2]); // read the updated info
		g_mpu[0] *= 180/PI;
		g_mpu[1] *= 180/PI;
		g_mpu[2] *= 180/PI;
		//populate the offset arrays
		offset_mpu[0] += (-g_mpu[0]*0.0175);
		offset_mpu[1] += (-g_mpu[1]*0.0175);
		offset_mpu[2] += (-g_mpu[2]*0.0175);
		//wait a bit before reading gyro again
		usleep(10000);}
	cout << "Calculating gyroscope offsets.........." << endl;
	// average the offsets for the mpu
	offset_mpu[0]/=100.0;
	offset_mpu[1]/=100.0;
	offset_mpu[2]/=100.0;
	cout << "Setting gyroscope offsets.............." << endl;
	// finally write the acquired offsets to the ahrs objects which have a member function which automatically handles
	// the application of offsets at each update/read cycle
	ahrs_mpu_madgwick.setGyroOffset(offset_mpu[0],offset_mpu[1],offset_mpu[2]);
	cout << " --Gyroscope offsets stored in AHRS--  " << endl;
	cout << "Setting magnetometer calibration......." << endl;
	ahrs_mpu_madgwick.setMagCalibration(mag_offset_mpu,mag_rotation_mpu);
	cout << "--Magnetometer offsets stored in AHRS--" << endl;
	cout << "-Magnetometer rotations stored in AHRS-" << endl;

	//------------------------------------------------------------------------------------------------------------------Welcome Message
	usleep(500000);
	cout << endl;
	cout << "=======================================" << endl;
	cout << "Initialization completed..............." << endl;
	cout << "=======================================" << endl << endl;
	usleep(500000);
	cout << "=======================================" << endl;
	cout << "Main Loop starting now................." << endl;
	cout << "=======================================" << endl << endl;
	usleep(500000);

	//----------------------------------------------------------------------------------------------------------Log File Initialization
	while(true)
	{
		int standby_message_timer = 0; // used to limit the frequency of the standby message

		while(!(rc_array[5]>1500)){ // uncomment here when using a transmitter
		// bool temp_flag = false; // uncomment here when no transmitter is used
		// while(!temp_flag){ // uncomment here when no transmitter is used
			if(standby_message_timer > 250){
				cout << endl;
				cout << "---------------------------------------" << endl;
				cout << "           Autopilot Inactive          " << endl;
				cout << "         Waiting for Killswitch        " << endl;
				cout << "---------------------------------------" << endl;
				standby_message_timer = 0;}

			standby_message_timer++;
//			pwm_out.set_duty_cycle(M1, 1);
	pwm_out.set_duty_cycle(M1, 1);
	pwm_out.set_duty_cycle(M2, 1);
	pwm_out.set_duty_cycle(M3, 1);
	pwm_out.set_duty_cycle(M4, 1);
			// since this loop executes based on an rc and an adc condition, we have to poll these devices for new status
			rc_array[5] = rcinput.read(5);
			adc_array[4] = adc.read(4);
			// step counter needs to be set to zero also, this is a hack because the numbering is messed up in the code
			// we start at negative one here and presumably the counter is incremented before 1st execution
			usleep(5000);
			// temp_flag = true;

		}
		time_t result = time(NULL);
		char *today = asctime(localtime(&result)); // establish char array to write today's date
		today[strlen(today) - 1] = '\0'; // remove end line from the end of the character array
		// remove spaces, remove colons, only keep the month/day/hour/minute
		for(int i = 0 ; i < FILENAME_LENGTH ; i++){
			if(today[i+FILENAME_OFFSET] == ' ' || today[i+FILENAME_OFFSET] == ':'){
				if(i == 8 - FILENAME_OFFSET) {
					filename[i] = '0';} // add leading zero in front of 1 digit day
				else{
					filename[i] = '_';}}
			else{
				filename[i] = today[i+FILENAME_OFFSET];}}
		// add .csv to the end of the file
		filename[FILENAME_LENGTH+0] = '-';
		filename[FILENAME_LENGTH+1] = '0';
		filename[FILENAME_LENGTH+2] = '.';
		filename[FILENAME_LENGTH+3] = 'c';
		filename[FILENAME_LENGTH+4] = 's';
		filename[FILENAME_LENGTH+5] = 'v';
		// for adding the relative path to the file, it will be converted to a string
		string filename_str(filename);
		//cout << "filename_str" << filename_str << endl;
		filename_str = logfile_prefix_string+filename_str;
		// used to put a number on the end of the file if it is a duplicate
		int filename_index = 1;
		// loop while the file name already exists or until we are out of indices to write to
		cout << endl << "Setting up log file...................." << endl;
		cout << "Checking for unique file name.........." << endl;
		while(file_exists(filename_str))
		{
		cout << "Filename already exists................" << endl;
			filename[FILENAME_LENGTH+0] = '-';
			filename[FILENAME_LENGTH+1] = filename_index + '0';
			filename[FILENAME_LENGTH+2] = '.';
			filename[FILENAME_LENGTH+3] = 'c';
			filename[FILENAME_LENGTH+4] = 's';
			filename[FILENAME_LENGTH+5] = 'v';
			string temp(filename);
			filename_str = logfile_prefix_string+temp;
			filename_index++;
			usleep(50000);} // don't try to read the files at warp speed
		// create the file output stream object
		ofstream fout;
		// open the file
		cout << "Log file created at: " << endl << filename_str << endl << endl;
		fout.open(filename_str,ios::out);
		// header string
		fout << "today,microseconds_since_start,"
			"msl,rc0,rc1,rc2,rc3,rc4,rc5,"
			"rc0_scaled,rc1_scaled,rc2_scaled,rc3_scaled,rc4_scaled,rc5_scaled,"
			"adc_array[0],adc_array[1],adc_array[2],adc_array[3],adc_array[4],adc_array[5],"
			"a_mpu[0],a_mpu[1],a_mpu[2],"
			"g_mpu[0],g_mpu[1],g_mpu[2],"
			"m_mpu[0],m_mpu[1],m_mpu[2],"
			"PITCH_CMD{38}KP="<<k_p<<"KI="<<k_i<<"KD="<<k_d<<",PITCH_MEAS{39},"
			"ROLL_CMD{40},ROLL_MEAS{41},"
			"YAW_CMD{42}KPy="<<k_py<<"KIy="<<k_iy<<"KDy="<<k_dy<<",YAW_MEAS{43},"<<endl;
		usleep(20000);


while((rc_array[5]>1500)) // uncomment here when using a transmitter
// while(true) // uncomment here when no transmitter is used
	{
		// refresh time now to prepare for another loop execution
		gettimeofday(&time_obj, NULL); // must first update the time_obj
		tse        = time_obj.tv_sec*1000000LL + time_obj.tv_usec; // update tse (us)
		time_now   = tse - time_start; // calculate the time since execution start by subtracting off tse

		if( (time_now-timer[0]) > duration[0])
		{
			//----------------------------------------------------------------------------------------------------------------AHRS Update
			dt = time_now-timer[0];
			dt = dt/1000000.0; // convert from useconds

			// Tested sampling rate for IMUs, with both IMUs execution of the following block was taking
			// approximate 1300us (~750Hz), slowed this loop down ot 500Hz so that there is a little
			// headroom but the sensor is being polled as quickly as possible
			// Read both IMUs at 500Hz
			// start with the MPU9250
			mpu->update();
			mpu->read_accelerometer(&a_mpu[0],&a_mpu[1],&a_mpu[2]);
			mpu->read_gyroscope(&g_mpu[0],&g_mpu[1],&g_mpu[2]);
			mpu->read_magnetometer(&m_mpu[0],&m_mpu[1],&m_mpu[2]);

			for(int i = 0 ; i < 3 ; i++ ){
				a_mpu_ahrs[i] = a_mpu[i]/G_SI;
				g_mpu_ahrs[i] = g_mpu[i]*(180/PI);}

			ahrs_mpu_madgwick.updateMadgwick(a_mpu_ahrs[0],a_mpu_ahrs[1],a_mpu_ahrs[2],g_mpu_ahrs[0]*0.0175,g_mpu_ahrs[1]*0.0175,g_mpu_ahrs[2]*0.0175,m_mpu[0],m_mpu[1],m_mpu[2],dt);

			watcher[0] = time_now - timer[0]; // used to check loop frequency
			timer[0] = time_now;
		}
		if( (time_now-timer[1]) > duration[1])
		{

			watcher[1] = time_now - timer[1];
			timer[1] = time_now;
		}

		if( (time_now-timer[2]) > duration[2])
		{
			watcher[2] = time_now - timer[2]; // used to check loop frequency
			timer[2] = time_now;
		}

		if( (time_now-timer[3]) > duration[3]) //=============================  100 Hz Loop ===============================
		{
			//-------------------------------------------------------------------------------------------------------------Barometer Read
			if(baro_step == 0){
				barometer.refreshPressure();}
			else if(baro_step == 1){
				barometer.readPressure();}
			else if(baro_step == 2){
				barometer.refreshTemperature();}
			else if(baro_step == 3){
				barometer.readTemperature();}
			else if(baro_step == 4){
				barometer.calculatePressureAndTemperature();
				baro_step = -1;}
			else{
				cout << "improper barometer step, pressure may be incorrect" << endl;}
			baro_step++; // increment the step

//----------------------------------------------------------------------------------------------------------------------------
//-------------------------------------------------- Begin Student Section  --------------------------------------------------
//----------------------------------------------------------------------------------------------------------------------------
	// STATE MEASUREMENTS
	pitch_m = pitch_mpu_madgwick;
	roll_m = roll_mpu_madgwick;
	yaw_m = g_mpu[2];

	// DESIRED COMMANDS
	// pitch_d = 0;
	pitch_d = rc_array_scaled[1];
	// roll_d = 0;
	roll_d = rc_array_scaled[0];
	// yaw_d = 0;
	yaw_d = rc_array_scaled[3];

	// THROTTLE COMMAND
	// throttle_cmd = 1.5;
	throttle_cmd = rc_array_scaled[2];

	for(int i = 0, i < 9, i++)
	{
		for(int j = OLS_PTS-1, j > 0, j--)
		{
			mem_pts[i][j-1] = mem_pts[i][j];
		}
	}
	mem_pts[0][0] = pitch_d;
	mem_pts[1][0] = roll_d;
	mem_pts[2][0] = yaw_d;
	mem_pts[3][0] = pitch_m;
	mem_pts[4][0] = roll_m;
	mem_pts[5][0] = yaw_m;
	mem_pts[6][0] = (pitch_m + pm_old)/100;
	mem_pts[7][0] = (roll_m + rm_old)/100;
	mem_pts[8][0] = (yaw_m + ym_old)/100;
	auto bilin_coefs = OLS_2var(mem_pts);
	// PITCH COEFFICIENTS
	// pitch_coef_a = std::get<0>(bilin_coefs)
	// pitch_coef_b = std::get<1>(bilin_coefs)
	// pitch_coef_c = std::get<2>(bilin_coefs)


	// PITCH ERROR CALC
	err_pp = pitch_d - pitch_m;
	err_pi = (err_pp + err_p_old)*0.005;
	err_pd = (err_pp - err_p_old)*100;

	// ROLL ERROR CALC
	err_rp = roll_d - roll_m;
	err_ri = (err_rp + err_r_old)*0.005;
	err_rd = (err_rp - err_r_old)*100;

	// YAW ERROR CALC
	err_yp = yaw_d - yaw_m;
	err_yi = (err_yp + err_y_old)*0.005;
	err_yd = (err_yp - err_y_old)*100;

	// CORRECTIVE COMMAND
	pit_lam = (err_pp * k_p) + (err_pi * k_i) + (err_pd * k_d);
	rol_lam = (err_rp * k_p) + (err_ri * k_i) + (err_rd * k_d);
	yaw_lam = (err_yp * k_py) + (err_yi * k_iy) + (err_yd * k_dy);

	p_dot = (pitch_m - p_old)*0.01; // slope = [f(x+h) - f(x)]/h => Finite difference

	pit_lam = (k_2*(pitch_d - pitch_m) + p_dot*((b_damp/I_mom) - p_dot)) / (2*k_torque/ I_mom);

	// ERROR STORAGE
	err_p_old = err_pp;
	err_r_old = err_rp;
	err_y_old = err_yp;
	p_old = pitch_m;

	// ELIMINATE BASELINE NOISE
	if (throttle_cmd < 1)
	{
	M1cmd = 0;
	M2cmd = 0;
	M3cmd = 0;
	M4cmd = 0;
	}

	// Generate output commands for motors
	M1cmd = throttle_cmd + pit_lam - yaw_lam;
	M2cmd = throttle_cmd - rol_lam + yaw_lam;
	M3cmd = throttle_cmd - pit_lam - yaw_lam;
	M4cmd = throttle_cmd + rol_lam + yaw_lam;

	// Signal overload protection
	if(M1cmd>2.0){
		M1cmd = 2.0;
	} else if (M1cmd < 1.0){
		M1cmd = 1.0;
		}
	if(M2cmd>2.0){
		M2cmd = 2.0;
	} else if (M2cmd < 1.0){
		M2cmd = 1.0;
		}
	if(M3cmd>2.0){
	M3cmd = 2.0;
	} else if (M3cmd < 1.0){
		M3cmd = 1.0;
		}
	if(M4cmd>2.0){
		M4cmd = 2.0;
	} else if (M4cmd < 1.0){
		M4cmd = 1.0;
		}
	// Send command to motors
	pwm_out.set_duty_cycle(M1,M1cmd);
	pwm_out.set_duty_cycle(M3,M3cmd);
	pwm_out.set_duty_cycle(M2,M2cmd);
	pwm_out.set_duty_cycle(M4,M4cmd);
	pm_old = pitch_m;
	rm_old = roll_m;
	ym_old = yaw_m;

//----------------------------------------------------------------------------------------------------------------------------
//--------------------------------------------------- End Student Section  ---------------------------------------------------
//----------------------------------------------------------------------------------------------------------------------------

			//--------------------------------------------------------------------------------------------------------------RC Input Read
			for(int i = 0 ; i < rcinput.channel_count ; i++ )
			{
				rc_array[i] = rcinput.read(i); // read in each value using the private class function (converts to int automatically)
				if(dbmsg_global || dbmsg_local) {cout << "Channel Number: " << i << " Channel Value: "  << rc_array[i] << endl;}
			}
			for(int i = 0 ; i < rcinput.channel_count ; i++)
			{
				rc_array_scaled[i] = scale_output(coefficients[i],float(rc_array[i]));
			}

			//-----------------------------------------------------------------------------------------------------------------ADC Update
			for(int i = 0 ; i < ARRAY_SIZE(adc_array) ; i++){
				adc_array[i] = adc.read(i);}

			//------------------------------------------------------------------------------------------------------Euler Angle Conversion
			ahrs_mpu_madgwick.getEuler(&roll_mpu_madgwick,&pitch_mpu_madgwick,&yaw_mpu_madgwick);

			//----------------------------------------------------------------------------------------------------------------Controllers
			float dt_control = time_now-timer[3]; // dt for this loop
			dt_control = dt_control/1000000.0; // convert from useconds

			//-------------------------------------------------------------------------------------------------------Data Log File Output
			fout << today << "," << time_now << "," << msl << ",";
			for(int i = 0 ; i < rcinput.channel_count ; i++){
				fout << rc_array[i] << ",";}
			for(int i = 0 ; i < rcinput.channel_count ; i++){
				fout << rc_array_scaled[i] << ",";}
			for(int i = 0 ; i < ARRAY_SIZE(adc_array) ; i++){
				fout << adc_array[i] << ",";}
			fout << a_mpu[0] << "," << a_mpu[1] << "," << a_mpu[2] << ",";
			fout << g_mpu[0] << "," << g_mpu[1] << "," << g_mpu[2] << ",";
			fout << m_mpu[0] << "," << m_mpu[1] << "," << m_mpu[2] << ",";
			fout << pitch_d << "," << pitch_m << ",";
			fout << roll_d << "," << roll_m << ",";
			fout << yaw_d << "," << yaw_m << ",";
			// add things to the log file here
			fout << endl;

			watcher[3] = time_now - timer[3]; // used to check loop frequency
			timer[3] = time_now;
		}

		if( (time_now-timer[4]) > duration[4])
		{
			//-------------------------------------------------------------------------------------------------------------Barometer Calc
			// barometer does full update at 25Hz, no need to do the full altitude calculation any faster than 50Hz
			Tc  = barometer.getTemperature(); // temperature from sensor (C), value is recorded at surface of PCB, (higher than ambient!)
			Tk  = Tc + 273.15; // convert to Kelvin (needed for barometric formula
			Tf  = Tc * (9.0/5.0) + 32; // convert to Fahrenheit (uncomment for sanity check but it is not used for any calcs)
			Pm  = barometer.getPressure(); // pressure is natively given in mbar
			Phg = Pm*.02953; // convert to inHg
			// barometric equation
			msl = hb + (Tb/Lb)*(pow((Phg/Pb),((-R*Lb)/(g0*M)))-1); // NOTE: using local Tk instead of standard temperature (Tb)

			if( dbmsg_global || dbmsg_local) {cout << "Barometer Check (at 50Hz), Temp (C,K,F): " << Tc << " " << Tk << " " << Tf << " "
				<< "Pressure (mbar, inHg): " << Pm << " " << Phg << " Altitude MSL (ft): " << msl << endl;}

			watcher[4] = time_now - timer[4]; // used to check loop frequency
			timer[4] = time_now;
		}


		if( (time_now-timer[5]) > duration[5]){
			watcher[5] = time_now - timer[5]; // used to check loop frequency
			timer[5] = time_now;}

		if( (time_now-timer[6]) > duration[6]){
			watcher[6] = time_now - timer[6]; // used to check loop frequency
			timer[6] = time_now;}

		if( (time_now-timer[7]) > duration[7]){
			watcher[7] = time_now - timer[7];
			timer[7] = time_now;}

		if( (time_now-timer[8]) > duration[8]){
			//Output Message
			//if(dbmsg_global || dbmsg_local){
			if(!dbmsg_global && !dbmsg_local){
				cout << endl;
				cout << "Current filename: " << filename_str << endl;
				cout << "Barometer Altitude: " << msl << " ft" << endl;
				cout << "Raw RC Input:";
				for(int i = 0 ; i < rcinput.channel_count ; i++ ){
					cout << " channel " << i << ": " << rc_array[i];
					if(i != rcinput.channel_count -1){
						cout << ",";}}
				cout << endl;
				cout << "Scaled RC Input:";
				for(int i = 0 ; i < rcinput.channel_count ; i++ ){
					cout << " channel " << i << ": " << rc_array_scaled[i];
					if(i != rcinput.channel_count -1){
						cout << ",";}}
				cout << endl;
				cout << "MPU9250: ";
				cout << "Accelerometer: " << a_mpu[0] << " " << a_mpu[1] << " " << a_mpu[2];
				cout << " Gyroscope: " << g_mpu[0] << " " << g_mpu[1] << " " << g_mpu[2];
				cout << " Magnetometer: " << m_mpu[0] << " " << m_mpu[1] << " " << m_mpu[2] << endl;
				// add console output messages here
				cout << endl;
			}


			//dbmsg_local = true;
			if(dbmsg_global || dbmsg_local){
				// Alternate debug message, just print out the most current duration for each loop occasionally
				cout << "Printing the most current expected vs. actual time since last execution for each loop" << endl;
				for(int i = 0 ; i < NUM_LOOPS ; i++){
					cout << "For " << frequency[i] << "(Hz) loop, expected: " << duration[i] << "(us), actual: " << watcher[i] << endl;}}
			//dbmsg_local = false;

			watcher[8] = time_now - timer[8]; // used to check loop frequency
			timer[8] = time_now;
		}

	}

	// tidy up and close the file when we exit the inner while loop
	fout.close();
	}
	return 0;
}
