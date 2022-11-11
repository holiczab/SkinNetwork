package com.example.skinapp;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.content.FileProvider;
import android.util.Base64;
import android.app.AlertDialog;
import android.content.ActivityNotFoundException;
import android.content.DialogInterface;
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
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;
import static android.Manifest.permission.READ_EXTERNAL_STORAGE;
import static android.Manifest.permission.WRITE_EXTERNAL_STORAGE;

import com.android.volley.RequestQueue;
import com.android.volley.toolbox.Volley;

import org.jetbrains.annotations.NotNull;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Calendar;
import java.util.Date;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class OnlineActivity extends AppCompatActivity {

    ImageButton menuButton,pdfButton,sendBtn;
    int pageHeight = 1120;
    int pagewidth = 792;
    Uri imageUri;
    Bitmap bmp, scaledbmp;
    ImageView kep;
    // constant code for runtime permissions
    private static final int PERMISSION_REQUEST_CODE = 200;
    private static final int PICK_IMAGE = 100;
    public String postUrl= "http://" + "192.168.0.25" + ":" + 8080 + "/predict";
    public String postBody= "";
    public JSONObject jsonString;
    public static final MediaType JSON = MediaType.parse("application/json; charset=utf-8");
    TextView name,percentage;
    ProgressBar progressBar;
    public static String encodeTobase64(Bitmap image) {
        Bitmap immagex=image;
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        immagex.compress(Bitmap.CompressFormat.JPEG, 100, baos);
        byte[] b = baos.toByteArray();
        String imageEncoded = Base64.encodeToString(b,Base64.DEFAULT);
        return imageEncoded;
    }
    public boolean isJSONValid(String test) {
        try {
            new JSONObject(test);
        } catch (JSONException ex) {
            // edited, to include @Arthur's comment
            // e.g. in case JSONArray is valid as well...
            try {
                new JSONArray(test);
            } catch (JSONException ex1) {
                return false;
            }
        }
        return true;
    }
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data){
        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode == RESULT_OK && requestCode == PICK_IMAGE){
            imageUri = data.getData();
            kep.setImageURI(imageUri);
            InputStream imageStream = null;
            try {
                imageStream = this.getContentResolver().openInputStream(imageUri);
                Bitmap yourSelectedImage = BitmapFactory.decodeStream(imageStream);
                jsonString = new JSONObject().put("image", encodeTobase64(yourSelectedImage));
                postRequest(postUrl, String.valueOf(jsonString));
            } catch (JSONException | IOException e) {
                e.printStackTrace();
            }
        }
        if (requestCode == 7 && resultCode == RESULT_OK) {
            Bitmap bitmap = (Bitmap) data.getExtras().get("data");
            kep.setImageBitmap(bitmap);
            try {
                jsonString = new JSONObject().put("image", encodeTobase64(bitmap));
                postRequest(postUrl, String.valueOf(jsonString));
            } catch (JSONException | IOException e) {
                e.printStackTrace();
            }
        }

    }

    void postRequest(String postUrl, String postBody) throws IOException {

        OkHttpClient client = new OkHttpClient();
        RequestBody body = RequestBody.create(JSON, postBody);
        //Log.i("Mytag", postBody);
        Request request = new Request.Builder()
                .header("client", "mobile")
                .url(postUrl)
                .post(body)
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(final Call call, final IOException e) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        Toast.makeText(OnlineActivity.this,
                                "Something went wrong:" + " " + e.getMessage(), Toast.LENGTH_LONG).show();
                        call.cancel();
                    }
                });
            }
            @Override
            public void onResponse(Call call, final Response response) throws IOException {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            //Toast.makeText(OnlineActivity.this,  response.body().string(), Toast.LENGTH_LONG).show();
                            JSONObject myObject = new JSONObject(response.body().string());
                            name.setText(myObject.get("prediction").toString());
                            percentage.setText(myObject.get("probability").toString().substring(2,4)+" %");
                            progressBar.setProgress(Integer.parseInt(myObject.get("probability").toString().substring(2,4)));
                        } catch (JSONException | IOException e) {
                            e.printStackTrace();
                        }
                    }
                });
            }
        });
    }

    private void openCamera() {
        Intent intent = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
        startActivityForResult(intent, 7);
    }
    private void openGallery() {
        Intent gallery = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.INTERNAL_CONTENT_URI);
        startActivityForResult(gallery, PICK_IMAGE);
    }
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_online);
        sendBtn=findViewById(R.id.sendBtn);
        kep=findViewById(R.id.imageView5);
        name=findViewById(R.id.name);
        percentage=findViewById(R.id.percentage);
        progressBar=findViewById(R.id.progressBar);
        bmp = BitmapFactory.decodeResource(getResources(), R.drawable.skin);
        scaledbmp = Bitmap.createScaledBitmap(bmp, 140, 140, false);
        if (checkPermission()) {
            //Toast.makeText(this, "Permission Granted", Toast.LENGTH_SHORT).show();
        } else {
            requestPermission();
        }
        DialogInterface.OnClickListener dialogClickListener = new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                switch (which){
                    case DialogInterface.BUTTON_POSITIVE:
                        openCamera();
                        break;

                    case DialogInterface.BUTTON_NEGATIVE:
                        openGallery();
                        break;
                }
            }
        };

        sendBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                AlertDialog.Builder builder = new AlertDialog.Builder(v.getContext());
                builder.setMessage("Where do you want to get the picture from?").setPositiveButton("Camera", dialogClickListener)
                        .setNegativeButton("Gallery", dialogClickListener).show();
            }
        });
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