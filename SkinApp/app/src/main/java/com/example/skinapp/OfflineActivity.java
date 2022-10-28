package com.example.skinapp;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.camera.core.Camera;
import androidx.camera.core.CameraSelector;
import androidx.camera.core.ImageAnalysis;
import androidx.camera.core.ImageProxy;
import androidx.camera.core.Preview;
import androidx.camera.lifecycle.ProcessCameraProvider;
import androidx.camera.view.LifecycleCameraController;
import androidx.camera.view.PreviewView;
import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.lifecycle.LifecycleOwner;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.renderscript.ScriptGroup;
import android.util.Log;
import android.util.Size;
import android.view.KeyEvent;
import android.view.View;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.common.util.concurrent.ListenableFuture;

import org.pytorch.IValue;
//import org.pytorch.LiteModuleLoader;
import org.pytorch.Module;
import org.pytorch.Tensor;
import org.pytorch.torchvision.TensorImageUtils;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

public class OfflineActivity extends AppCompatActivity {

    ImageButton loadBtn, cameraBtn;
    private static final int PICK_IMAGE = 100;
    Uri imageUri;
    public static final int RequestPermissionCode = 1;
    ImageButton menuButton,liveBtn;
    Classifier classifier;
    ImageView kep;
    TextView name,percentage;
    private ListenableFuture<ProcessCameraProvider> cameraProviderFuture;
    PreviewView previewView;
    TextView textView;
    ConstraintLayout camlay;
    ProcessCameraProvider cameraProvider;
    private int REQUEST_CODE_PERMISSION=101;
    private final String[] REQUIRED_PERMISSIONS=new String[]{"android.permission.CAMERA"};
    List<String> imagenet_classes;

    private boolean checkPermissions(){
        for (String permission: REQUIRED_PERMISSIONS){
            if(ContextCompat.checkSelfPermission(this,permission)!=PackageManager.PERMISSION_GRANTED){
                return false;
            }
        }
        return true;
    }
    Executor executor= Executors.newSingleThreadExecutor();
    void startCamera(@NonNull ProcessCameraProvider cameraProvider){
        Preview preview = new Preview.Builder().build();
        CameraSelector cameraSelector=new CameraSelector.Builder().requireLensFacing(CameraSelector.LENS_FACING_BACK).build();
        preview.setSurfaceProvider(previewView.getSurfaceProvider());

        ImageAnalysis imageAnalysis=new ImageAnalysis.Builder()
                .setTargetResolution(new Size(224,224))
                .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST).build();
        imageAnalysis.setAnalyzer(executor, new ImageAnalysis.Analyzer() {
            @Override
            public void analyze(@NonNull ImageProxy image) {
                int rotation=image.getImageInfo().getRotationDegrees();
                analyzeImage(image,rotation);
                image.close();
            }
        });

        Camera camera=cameraProvider.bindToLifecycle((LifecycleOwner) this,cameraSelector,preview,imageAnalysis);
    }
    Module module;
    void LoadTorchModule(String fileName) {
        File modelFile = new File(this.getFilesDir(), fileName);
        try {
            if(!modelFile.exists()){
                InputStream inputStream=getAssets().open(fileName);
                FileOutputStream outputStream=new FileOutputStream(modelFile);
                byte[] buffer=new byte[2048];
                int bytesRead=-1;
                while((bytesRead=inputStream.read(buffer))!=-1){
                    outputStream.write(buffer,0,bytesRead);
                }
                inputStream.close();
                outputStream.close();
            }
            module = Module.load(modelFile.getAbsolutePath());
        }
        catch (IOException e){
            e.printStackTrace();
        }
    }

    void analyzeImage(ImageProxy image,int rotation){
        @SuppressLint("UnsafeOptInUsageError") Tensor inputTensor= TensorImageUtils.imageYUV420CenterCropToFloat32Tensor(image.getImage(), rotation,224,224,
                TensorImageUtils.TORCHVISION_NORM_MEAN_RGB,TensorImageUtils.TORCHVISION_NORM_STD_RGB);
        Tensor outputTensor=module.forward(IValue.from(inputTensor)).toTensor();
        float[] scores=outputTensor.getDataAsFloatArray();
        float maxScore=-Float.MAX_VALUE;
        int maxScoreIdx=-1;
        for (int i=0;i<scores.length;i++){
            if(scores[i]>maxScore){
                maxScore=scores[i];
                maxScoreIdx=i;
            }
        }

        String classResult=imagenet_classes.get(maxScoreIdx);
        Log.v("Torch","Detected - "+classResult);
        float finalMaxScore = maxScore;
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                textView.setText(classResult+" - "+ finalMaxScore +"%");
            }
        });

    }
    List<String> LoadClasses(String fileName){
        List<String> classes=new ArrayList<>();

        try {
            BufferedReader br = new BufferedReader(new InputStreamReader(getAssets().open(fileName)));
            String line;
            while((line=br.readLine())!=null){
                classes.add(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return classes;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_offline);
        imagenet_classes=LoadClasses("imagenet-classes.txt");
        previewView=findViewById(R.id.cameraView);
        textView=findViewById(R.id.result_text);
        camlay=findViewById(R.id.camlay);
        if(!checkPermissions()){
            ActivityCompat.requestPermissions(this,REQUIRED_PERMISSIONS,REQUEST_CODE_PERMISSION);
        }
        LoadTorchModule("mobilenet-v2.pt");
        cameraProviderFuture=ProcessCameraProvider.getInstance(this);
        cameraProviderFuture.addListener(()-> {
            try {
                cameraProvider = cameraProviderFuture.get();
                startCamera(cameraProvider);

            }
            catch (ExecutionException | InterruptedException e) { }
        },ContextCompat.getMainExecutor(this));

        liveBtn=findViewById(R.id.liveBtn);
        liveBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                camlay.setVisibility(View.VISIBLE);
            }
        });

        kep=findViewById(R.id.imageView5);
        loadBtn = findViewById(R.id.loadBtn);
        name = findViewById(R.id.textView9);
        percentage = findViewById(R.id.textView10);

        loadBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openGallery();
            }
        });
        classifier = new Classifier(Utils.assetFilePath(this,"mobilenet-v2.pt"));
        cameraBtn = findViewById(R.id.cameraBtn);
        cameraBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openCamera();
            }
        });
        menuButton = findViewById(R.id.backButton);
        menuButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(OfflineActivity.this,AllDiagnosesActivity.class));
            }
        });


    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (event.getKeyCode() == KeyEvent.KEYCODE_BACK && event.getRepeatCount() == 0) {
            cameraProvider.unbindAll();
            finish();
            startActivity(new Intent(getApplicationContext(), OfflineActivity.class));
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }

    private void openGallery() {
        Intent gallery = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.INTERNAL_CONTENT_URI);
        startActivityForResult(gallery, PICK_IMAGE);
    }
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data){
        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode == RESULT_OK && requestCode == PICK_IMAGE){
            imageUri = data.getData();
            kep.setImageURI(imageUri);
            Bitmap bitmap = null;
            try {
                bitmap = MediaStore.Images.Media.getBitmap(this.getContentResolver(), imageUri);
            } catch (IOException e) {
                e.printStackTrace();
            }
            name.setText(classifier.predict(bitmap)[0]);
            percentage.setText(classifier.predict(bitmap)[1]);

        }
        if (requestCode == 7 && resultCode == RESULT_OK) {
            Bitmap bitmap = (Bitmap) data.getExtras().get("data");
            kep.setImageBitmap(bitmap);
            name.setText(classifier.predict(bitmap)[0]);
            percentage.setText(classifier.predict(bitmap)[1]);

        }

    }
    private void openCamera() {
        Intent intent = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
        startActivityForResult(intent, 7);
    }

    public void EnableRuntimePermission(){
        if (ActivityCompat.shouldShowRequestPermissionRationale(OfflineActivity.this,
                Manifest.permission.CAMERA)) {
            Toast.makeText(OfflineActivity.this,"CAMERA permission allows us to Access CAMERA app",     Toast.LENGTH_LONG).show();
        } else {
            ActivityCompat.requestPermissions(OfflineActivity.this,new String[]{
                    Manifest.permission.CAMERA}, RequestPermissionCode);
        }
    }
    @Override
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] result) {
        super.onRequestPermissionsResult(requestCode, permissions, result);
        switch (requestCode) {
            case RequestPermissionCode:
                if (result.length > 0 && result[0] == PackageManager.PERMISSION_GRANTED) {
                    Toast.makeText(OfflineActivity.this, "Permission Granted, Now your application can access CAMERA.", Toast.LENGTH_LONG).show();
                } else {
                    Toast.makeText(OfflineActivity.this, "Permission Canceled, Now your application cannot access CAMERA.", Toast.LENGTH_LONG).show();
                }
                break;
        }
    }
}