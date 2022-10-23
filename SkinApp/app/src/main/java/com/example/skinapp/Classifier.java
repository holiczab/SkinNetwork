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
        return TensorImageUtils.bitmapToFloat32Tensor(bitmap,this.mean,this.std);

    }

    public int[] argMax(float[] inputs){

        int maxIndex = -1;
        float maxvalue = 0.0f;

        for (int i = 0; i < inputs.length; i++){

            if(inputs[i] > maxvalue) {

                maxIndex = i;
                maxvalue = inputs[i];
            }

        }

        return new int[]{maxIndex, (int) maxvalue};
    }

    public String[] predict(Bitmap bitmap){

        Tensor tensor = preprocess(bitmap,224);

        IValue inputs = IValue.from(tensor);
        Tensor outputs = model.forward(inputs).toTensor();
        float[] scores = outputs.getDataAsFloatArray();
        int classIndex = argMax(scores)[0];

        for (int j=0;j<scores.length;j++)
            Log.i("Mytag", String.valueOf(scores[j]));

        String[] a={Constants.IMAGENET_CLASSES[classIndex],argMax(scores)[1]+" %"};
        return a;

    }

}
