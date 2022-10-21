package com.example.skinapp;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.content.FileProvider;

import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Typeface;
import android.graphics.pdf.PdfDocument;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.view.View;
import android.widget.ImageButton;
import android.widget.Toast;
import static android.Manifest.permission.READ_EXTERNAL_STORAGE;
import static android.Manifest.permission.WRITE_EXTERNAL_STORAGE;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Calendar;
import java.util.Date;

public class OnlineActivity extends AppCompatActivity {

    ImageButton menuButton,pdfButton;
    int pageHeight = 1120;
    int pagewidth = 792;

    Bitmap bmp, scaledbmp;

    // constant code for runtime permissions
    private static final int PERMISSION_REQUEST_CODE = 200;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_online);
        bmp = BitmapFactory.decodeResource(getResources(), R.drawable.skin);
        scaledbmp = Bitmap.createScaledBitmap(bmp, 140, 140, false);
        if (checkPermission()) {
            //Toast.makeText(this, "Permission Granted", Toast.LENGTH_SHORT).show();
        } else {
            requestPermission();
        }

        menuButton = findViewById(R.id.backButton);
        menuButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(OnlineActivity.this,AllDiagnosesActivity.class));
            }
        });
        pdfButton = findViewById(R.id.pdfButton);
        pdfButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                PdfDocument pdfDocument = new PdfDocument();

                Paint paint = new Paint();
                Paint title = new Paint();

                PdfDocument.PageInfo mypageInfo = new PdfDocument.PageInfo.Builder(pagewidth, pageHeight, 1).create();

                PdfDocument.Page myPage = pdfDocument.startPage(mypageInfo);

                Canvas canvas = myPage.getCanvas();

                canvas.drawBitmap(scaledbmp, 56, 40, paint);

                title.setTypeface(Typeface.create(Typeface.DEFAULT, Typeface.NORMAL));

                title.setTextSize(15);

                title.setColor(ContextCompat.getColor(OnlineActivity.this, R.color.purple_200));

                canvas.drawText("SKIN NETWORK", 209, 100, title);
                canvas.drawText("Skin disease diagnoses", 209, 80, title);

                title.setTypeface(Typeface.defaultFromStyle(Typeface.NORMAL));
                title.setColor(ContextCompat.getColor(OnlineActivity.this, R.color.purple_200));
                title.setTextSize(15);
                title.setTextAlign(Paint.Align.CENTER);
                canvas.drawText("This is sample document which we have created.", 396, 560, title);
                pdfDocument.finishPage(myPage);
                Date currentTime = Calendar.getInstance().getTime();
                File file = new File(Environment.getExternalStorageDirectory(), "Diagnoses_"+currentTime+".pdf");

                try {
                    pdfDocument.writeTo(new FileOutputStream(file));
                    Toast.makeText(OnlineActivity.this, "PDF file generated successfully.", Toast.LENGTH_SHORT).show();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                pdfDocument.close();
            }
        });

    }
    private boolean checkPermission() {
        // checking of permissions.
        int permission1 = ContextCompat.checkSelfPermission(getApplicationContext(), WRITE_EXTERNAL_STORAGE);
        int permission2 = ContextCompat.checkSelfPermission(getApplicationContext(), READ_EXTERNAL_STORAGE);
        return permission1 == PackageManager.PERMISSION_GRANTED && permission2 == PackageManager.PERMISSION_GRANTED;
    }

    private void requestPermission() {
        // requesting permissions if not provided.
        ActivityCompat.requestPermissions(this, new String[]{WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE}, PERMISSION_REQUEST_CODE);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == PERMISSION_REQUEST_CODE) {
            if (grantResults.length > 0) {

                // after requesting permissions we are showing
                // users a toast message of permission granted.
                boolean writeStorage = grantResults[0] == PackageManager.PERMISSION_GRANTED;
                boolean readStorage = grantResults[1] == PackageManager.PERMISSION_GRANTED;

                if (writeStorage && readStorage) {
                    //Toast.makeText(this, "Permission Granted..", Toast.LENGTH_SHORT).show();
                } else {
                    Toast.makeText(this, "Permission Denied.", Toast.LENGTH_SHORT).show();
                }
            }
        }
    }
}