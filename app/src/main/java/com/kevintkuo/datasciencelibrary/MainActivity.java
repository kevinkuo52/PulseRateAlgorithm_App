package com.kevintkuo.datasciencelibrary;

import android.Manifest;
import android.os.Environment;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.Toast;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;


import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Arrays;


import static_proxy.PyMathLib.*;
public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Get runtime permission for writing to csv
        ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1);
        //write to csv:
        //writeToFile("testCSV", "1.0,2.3\n4.0,5.0,6.0\n");

        if (! Python.isStarted()) {
            Python.start(new AndroidPlatform(getApplicationContext()));
        }
        Python py = Python.getInstance();

        PyObject BA = py.getModule("static_proxy.PyMathLib").get("Butter");

        PyObject ba_po = BA.call();
        Butter ba = ba_po.toJava(Butter.class);


        //Dummy data
        double[] data = {1.0,3.1,1.0,1.9,2.0,1.0,2.0,1.5,2.0};




        PyObject NS = py.getModule("static_proxy.PyMathLib").get("NpScipy");
        PyObject ns_po = NS.call();
        NpScipy npScipy = ns_po.toJava(NpScipy.class);





        double[][] detrend = npScipy.get_detrend(data,true);

        String d1 = Arrays.toString(detrend[0]);
        String d2 = Arrays.toString(detrend[1]);




        double[][] y = npScipy.butter_bandpass_filter(detrend, 0.75,4.0, 30.0, 4);
        String y1 = Arrays.toString(y[0]);
        String y2 = Arrays.toString(y[1]);



        double[][] powerSpec = npScipy.get_powerSpec(y, true);
        String p1 = Arrays.toString(powerSpec[0]);
        String p2 = Arrays.toString(powerSpec[1]);



        double[] freq = npScipy.fftfreq(150, (1.0/30));
        String f = Arrays.toString(freq);




        Button btn = findViewById(R.id.button);
        String outputString = "detrend\n"+d1+d2+"\n\n"+"butterworth bandpass filter\n"+y1+y2+"\n\n"+"powerSPec(np.fit.fit)\n"
                +p1+p2+"\n\n"+"freq (fftfreq)\n"+f;
        ShewchuksDeterminant sd = new ShewchuksDeterminant();
        Coordinate A = new Coordinate(0,0);
        Coordinate B = new Coordinate(10,0);
        Coordinate C = new Coordinate(10,-10);
        //sd.orient2d(A,B,C)

        double[] s1 = {1.0,2.0};
        double[] s2 = {7.0,3.0};
        double[] s3 = {9.0,10.0};
        double[] s4 = {18.0,17.0};
        double[][] pts = {{12.0,1.0},{10.0,18.0},{180.0,1.0},{28.0,1.0},{18.0,17.0},{19.0,19.0},{17.0,8.0},{20.0,17.0},{1800.0,17.0},{14.0,17.0},{1.0,17.0},
                {100.0,1.0},{18.0,1.0},{1.0,11.0},{1.0,7.0}};
        btn.setText(Arrays.toString(npScipy.py_kalman_filter(s1, s2, s3, s4, pts, true)[0])+","+Arrays.toString(npScipy.py_kalman_filter(s1, s2, s3, s4, pts, true)[1]));
    }

    public  void writeToFile(String fileName, String body)
    {
        FileOutputStream fos = null;

        try {
            final File dir = new File(Environment.getExternalStorageDirectory().getAbsolutePath());

            if (!dir.exists())
            {
                if(!dir.mkdirs()){
                    Log.e("ALERT","could not create the directories");
                }
            }

            final File myFile = new File(dir, fileName + ".csv");

            if (!myFile.exists())
            {
                myFile.createNewFile();
            }

            fos = new FileOutputStream(myFile);

            fos.write(body.getBytes());
            fos.close();
            Toast.makeText(getBaseContext(),
                    "Done writing SD"+Environment.getExternalStorageDirectory().getAbsolutePath(),
                    Toast.LENGTH_SHORT).show();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            Toast.makeText(getBaseContext(), e.getMessage(),
                    Toast.LENGTH_SHORT).show();
        }
    }
}
