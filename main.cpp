#include <iostream>
#include <vector>
#include <filesystem>
#include <fstream>
#include <string>
#include <sstream>
#include <mysql/mysql.h>
class EnvironmentData{

public: // start public here
    std::string m_sHumidity = "";
    std::string m_sTemperature = "";
    std::string m_sPressure = "";
    float m_fHumidity = 0.0;
    float m_fTemperature = 0.0;
    float m_fPressure = 0.0;


    std::string getHumidity()
    {
        return this->m_sHumidity;
    }

    std::string getPressure()
    {
        return this->m_sPressure;
    }

    std::string getTemperature()
    {
        return this->m_sPressure;
    }

    void setHumidity(std::string sHumid)
    {
        this->m_sHumidity = sHumid;
    }

    void setPressure(std::string sPressure)
    {
        this->m_sPressure = sPressure;
    }

    void setTemperature(std::string sTemp)
    {
        this->m_sTemperature = sTemp;
    }

    void toFloat()
    {
        if(this->m_sPressure.length() > 0 && this->m_sHumidity.length() > 0 && this->m_sTemperature.length() > 0) {
            this->m_fHumidity = atof(this->m_sHumidity.c_str());
            this->m_fPressure = atof(this->m_sPressure.c_str());
            this->m_fTemperature = atof(this->m_sTemperature.c_str());
        }
    }

    void toString()
    {
        std::cout<<
        "Temperature: "<<this->m_sTemperature<<std::endl<<
        "Humidity: " << this->m_sHumidity<<std::endl<<
        "Pressure: " << this->m_sPressure<<std::endl;
    }

    void ToFloatingString()
    {
        this->toFloat();
        std::cout<<"Temperature: " << this->m_fTemperature << std::endl
        << "Humidity:  " << this->m_fHumidity << std::endl<<
        "Pressure:  " << this->m_fPressure<<std::endl;
    }
};

// function prototypes
void getDataFromPi(EnvironmentData&);
void executePython();
void storeToDB();
int main() {
    executePython();
    EnvironmentData ed;
    getDataFromPi(ed);
    ed.ToFloatingString();
    //storeToDB();
    return 0;
}

void executePython()
{
    system("python main.py");
}

void getDataFromPi(EnvironmentData &ed)
{
    std::string sFileName = "/home/pi/Warehouse/Sense_data.csv"; // location of files
    //std::string sFileName = "C:\\temp\\Sense_data.csv";
    std::string sLine;
    std::fstream fin;
    std::vector<std::string> row;
    std::string myline,word,temp;
    fin.open(sFileName);
    fin >> myline;
    if ( fin.is_open() ) {
        std::vector <std::string> tokens;
        std::stringstream check1(myline);
        std::string sIntermediate;
        while(getline(check1, sIntermediate, ',')) {
            tokens.push_back(sIntermediate);
        }
        ed.setTemperature(tokens[0]);
        ed.setHumidity(tokens[1]);
        ed.setPressure(tokens[2]);
    }
    fin.close();
}

void storeToDB()
{
	MYSQL *conn;
	MYSQL_RES *res;
	MYSQL_ROW row;
	char *server = "localhost";
	char *user = "root";
	char *password = "toor";
	char *database = "data";

	if (!mysql_real_connect(conn, server, user, password,database, 0, NULL, 0)){
		fprintf(stderr, "%s\n", mysql_error(conn));
		exit(1);
	}

	if(mysql_query(conn, "show tables;")){
		exit(2);
	}
	res = mysql_use_result(conn);

	printf("Tables in db :\n");

	while((row = mysql_fetch_row(res)) != NULL){
		printf("%s \n", row[0]);

	}

	mysql_free_result(res);
	mysql_close(conn);

}

