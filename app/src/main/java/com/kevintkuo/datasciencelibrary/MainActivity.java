package com.kevintkuo.datasciencelibrary;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;

import java.util.Arrays;
import static_proxy.PyMathLib.*;
public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Python py = Python.getInstance();

        PyObject BA = py.getModule("static_proxy.PyMathLib").get("Butter");
        PyObject ba_po = BA.call();
        Butter ba = ba_po.toJava(Butter.class);


        //Dummy data
        double[][] data = {{1.0,3.1,1.0,1.9,2.0,1.0,2.0,1.5,2.0},{1.0,3.0,1.3,1.0,2.0,1.7,1.0,2.0,2.0}};
        double[][] y = ba.butter_bandpass_filter(data, 0.75,4.0, 30.0, 4);
        String y1 = Arrays.toString(y[0]);
        String y2 = Arrays.toString(y[1]);



        PyObject NS = py.getModule("static_proxy.PyMathLib").get("NpScipy");
        PyObject ns_po = NS.call();
        NpScipy npScipy = ns_po.toJava(NpScipy.class);



        double[][] powerSpec = npScipy.get_powerSpec(y, true);

        String p1 = Arrays.toString(powerSpec[0]);
        String p2 = Arrays.toString(powerSpec[1]);

        double[] freq = npScipy.fftfreq(150, (1.0/30));
        String f = Arrays.toString(freq);


        Button btn = findViewById(R.id.button);
        String outputString = "butterworth bandpass filter\n"+y1+y2 +"\n\n"+"powerSPec(np.fit.fit)\n"
                +p1+p2+"\n\n"+"freq (fftfreq)\n"+f;
        btn.setText(outputString);
    }
}
