package com.example.skinapp;

import android.graphics.Bitmap;
import android.util.Log;

import org.pytorch.Tensor;
import org.pytorch.Module;
import org.pytorch.IValue;
import org.pytorch.torchvision.TensorImageUtils;

import java.util.Arrays;


public class Classifier {

    Module model;
    float[] mean = {0.485f, 0.456f, 0.406f};
    float[] std = {0.229f, 0.224f, 0.225f};

    public Classifier(String modelPath){

        model = Module.load(modelPath);

    }

    public void setMeanAndStd(float[] mean, float[] std){

        this.mean = mean;
        this.std = std;
    }

    public Tensor preprocess(Bitmap bitmap, int size){

        bitmap = Bitmap.createScaledBitmap(bitmap,size,size,false);
        return TensorImageUtils.bitmapToFloat32Tensor(bitmap,
                TensorImageUtils.TORCHVISION_NORM_MEAN_RGB, TensorImageUtils.TORCHVISION_NORM_STD_RGB);

    }

    public int[] argMax(float[] inputs){

        int maxIndex = -1;
        float maxvalue = 0.0f;

        for (int i = 0; i < 7; i++){ //inputs.length

            if(inputs[i] > maxvalue) {

                maxIndex = i;
                maxvalue = inputs[i];
            }

        }

        return new int[]{maxIndex, (int) maxvalue};
    }

    public String[] predict(Bitmap bitmap){

        Tensor tensor = preprocess(bitmap,480);
        IValue[] outputTensor = model.forward(IValue.from(tensor)).toTuple();
        float[] scores = outputTensor[0].toTensor().getDataAsFloatArray();
        Log.i("Mytag", String.valueOf(scores.length));
        int classIndex = argMax(scores)[0];
        /*
        String g="";
        for (int j=0;j<scores.length;j++)
        {
            g+=" "+scores[j]+",";
        }
        Log.i("Mytag", g);
        */
        String[] a={Constants.IMAGENET_CLASSES[classIndex],argMax(scores)[1]+" %"};
        return a;

    }

}
