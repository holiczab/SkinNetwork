package com.example.skinapp;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.content.FileProvider;

import android.annotation.SuppressLint;
import android.graphics.drawable.BitmapDrawable;
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
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class OnlineActivity extends AppCompatActivity {

    ImageButton menuButton,pdfButton,sendBtn,emailBtn;
    int pageHeight = 1120;
    int pagewidth = 792;
    Uri imageUri;
    Bitmap bmp, scaledbmp;
    ImageView kep;

    // constant code for runtime permissions
    private static final int PERMISSION_REQUEST_CODE = 200;
    private static final int PICK_IMAGE = 100;
    public String postUrl= "http://" + "192.168.119.148"+ ":" + 8080 + "/predict";
    public String postBody= "";
    public JSONObject jsonString;
    public static final MediaType JSON = MediaType.parse("application/json; charset=utf-8");
    public String CURRENT_PDF="";
    TextView name,percentage,gyogy,leiras;
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
                                "Hiba történt:" + " " + e.getMessage(), Toast.LENGTH_LONG).show();
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
                            Log.i("Mytag",myObject.get("prediction").toString());
                            legyogy(myObject.get("prediction").toString());

                        } catch (JSONException | IOException e) {
                            e.printStackTrace();
                        }
                    }
                });
            }
        });
    }
    public void legyogy(String name){
        if (name.equals("Melanocytic nevi")){
            gyogy.setText("Műtét");
            leiras.setText("A melanocitikus nevus (más néven nevus nevus, nevus-cell nevus és általában anyajegy) egyfajta melanocitikus daganat, amely nevus sejteket tartalmaz.");
        }
        else if (name.equals("Melanoma")){
            gyogy.setText("Dacarbazine");
            leiras.setText("A melanóma vagy melanoma malignum a bőr pigmenttermelő sejtjeiből (melanocyta) kiinduló rosszindulatú daganat. Kialakulhat már meglévő anyajegyből különösen akkor, ha az állandó károsító ingernek van kitéve (erős UV sugárzás, mechanikai ártalom), de megjelenhet anyajegymentes bőrfelületen is.\n -");
        }
        else if (name.equals("Benign keratosis-like lesion")){
            gyogy.setText("Nincs szükség rá");
            leiras.setText("A seborrhoeás keratosis (seb-o-REE-ik ker-uh-TOE-sis) egy gyakori jóindulatú bőrnövekedés, hasonlóan az anyajegyhez. A legtöbb embernek élete során lesz legalább egy. Általában a felnőttkor közepén jelennek meg, és gyakoriságuk az életkorral növekszik.\n -");
        }
        else if (name.equals("Basal cell carcinoma")){
            gyogy.setText("Topical antineoplastic");
            leiras.setText("A bazálissejtes karcinóma a bőrrák egy fajtája, amely leggyakrabban a napsugárzásnak kitett bőrterületeken, például az arcon alakul ki. A barna és fekete bőrön a bazálissejtes karcinóma gyakran úgy néz ki, mint egy barna vagy fényes fekete dudor, amelynek szegélye van.\n -");
        }
        else if (name.equals("Actinic keratose")){
            gyogy.setText("Fluorouracil, Imiquimod");
            leiras.setText("Az aktinikus keratózisok (más néven szoláris keratózisok) száraz, pikkelyes bőrfoltok, amelyeket a nap károsított. A foltok általában nem súlyosak. De van egy kis esély, hogy bőrrákká váljanak, ezért fontos, hogy elkerülje a bőr további károsodását.\n -");
        }
        else if (name.equals("Vascular lesion")){
            gyogy.setText("Prednisone,  Propranolol");
            leiras.setText("Az érrendszeri elváltozások a bőr és a mögöttes szövetek viszonylag gyakori rendellenességei, ismertebb nevén anyajegyek.\n -");
        }
        else if (name.equals("Dermatofibroma")){
            gyogy.setText("Műtét");
            leiras.setText("A különösen nőknél gyakran előforduló jóindulatú, a bőr felszínéből kiemelkedő csomó, a dermatofibromának vagy fibrosus histiocytomának nevezett elváltozás.\n -");
        }
        else{
            gyogy.setText("Nem meghatározható");
            leiras.setText(" \n -");
        }
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
        gyogy=findViewById(R.id.gyogy);
        leiras=findViewById(R.id.leiras);
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
                builder.setMessage("Honnan szeretnéd feltölteni a képet?").setPositiveButton("Kamera", dialogClickListener)
                        .setNegativeButton("Galéria", dialogClickListener).show();
                pdfButton.setEnabled(true);
            }
        });
        menuButton = findViewById(R.id.backButton);
        menuButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(OnlineActivity.this,AllDiagnosesActivity.class));
            }
        });
        emailBtn = findViewById(R.id.emailBtn);
        emailBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

            }
        });

        pdfButton = findViewById(R.id.pdfButton);
        pdfButton.setEnabled(false);
        pdfButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                PdfDocument pdfDocument = new PdfDocument();

                Paint paint = new Paint();
                Paint title = new Paint();
                Paint a = new Paint();
                Paint b = new Paint();
                Paint c = new Paint();
                Paint d = new Paint();
                Paint de = new Paint();

                PdfDocument.PageInfo mypageInfo = new PdfDocument.PageInfo.Builder(pagewidth, pageHeight, 1).create();

                PdfDocument.Page myPage = pdfDocument.startPage(mypageInfo);

                Canvas canvas = myPage.getCanvas();

                title.setTypeface(Typeface.create(Typeface.DEFAULT, Typeface.NORMAL));
                title.setTextSize(30);
                title.setTextAlign(Paint.Align.LEFT);
                title.setColor(ContextCompat.getColor(OnlineActivity.this, R.color.teal_700));

                canvas.drawText("SKIN NETWORK - Bőrprobléma diagnózis", 70, 50, title);


                kep.buildDrawingCache(true);
                Bitmap bit = kep.getDrawingCache(true);
                Bitmap resizedBitmap = Bitmap.createScaledBitmap(bit, 300, 100, false);

                canvas.drawBitmap(resizedBitmap, 400, 130, paint);
                kep.destroyDrawingCache();

                a.setTypeface(Typeface.defaultFromStyle(Typeface.NORMAL));
                a.setColor(ContextCompat.getColor(OnlineActivity.this, R.color.black));
                a.setTextSize(20);
                a.setTextAlign(Paint.Align.LEFT);
                canvas.drawText("Név: "+name.getText(), 70, 150, a);

                b.setTypeface(Typeface.defaultFromStyle(Typeface.NORMAL));
                b.setColor(ContextCompat.getColor(OnlineActivity.this, R.color.black));
                b.setTextSize(20);
                b.setTextAlign(Paint.Align.LEFT);
                canvas.drawText("Pontosság: "+percentage.getText(),70,200, b);

                c.setTypeface(Typeface.defaultFromStyle(Typeface.NORMAL));
                c.setColor(ContextCompat.getColor(OnlineActivity.this, R.color.black));
                c.setTextSize(20);
                c.setTextAlign(Paint.Align.LEFT);
                canvas.drawText("Gyógyszer: "+gyogy.getText(), 70,250, c);

                d.setTypeface(Typeface.defaultFromStyle(Typeface.NORMAL));
                d.setColor(ContextCompat.getColor(OnlineActivity.this, R.color.black));
                d.setTextSize(20);
                d.setTextAlign(Paint.Align.LEFT);
                String newl="";
                String l= String.valueOf(leiras.getText());
                String arr [] = l.split(" ");
                int uj=300;
                for (int i=0;i<arr.length;i++)
                {
                    newl+=arr[i]+" ";
                    if(i%7==0 && i!=0) {
                        uj+=20;
                        canvas.drawText(newl, 70,uj, d);
                        newl="";
                    }
                }
                uj+=20;
                canvas.drawText(newl, 70,uj, d);
                de.setTypeface(Typeface.defaultFromStyle(Typeface.NORMAL));
                de.setColor(ContextCompat.getColor(OnlineActivity.this, R.color.design_default_color_error));
                de.setTextSize(10);
                de.setTextAlign(Paint.Align.LEFT);
                canvas.drawText("Ez az eszköz nem nyújt orvosi tanácsot, csak tájékoztató jellegű.", 70,uj+315, de);
                canvas.drawText("Nem helyettesíti a professzionális orvosi tanácsot, diagnózist vagy kezelést.", 70,uj+330, de);
                canvas.drawText("Mindig kérje orvosa vagy más képzett egészségügyi szakember útmutatását,", 70,uj+345, de);
                canvas.drawText("ha bármilyen kérdése van az egészségével vagy egészségügyi állapotával kapcsolatban.", 70,uj+360, de);

                pdfDocument.finishPage(myPage);
                Date currentTime = Calendar.getInstance().getTime();
                File file = new File(Environment.getExternalStorageDirectory(), "Diagnoses_"+currentTime+".pdf");

                CURRENT_PDF="Diagnoses_"+currentTime+".pdf";

                Intent viewPdf = new Intent(Intent.ACTION_VIEW);
                viewPdf.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_NEW_TASK);
                Uri URI = FileProvider.getUriForFile(OnlineActivity.this, OnlineActivity.this.getApplicationContext().getPackageName() + ".provider", file);
                viewPdf.setDataAndType(URI, "application/pdf");
                viewPdf.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                OnlineActivity.this.startActivity(viewPdf);
                try {
                    pdfDocument.writeTo(new FileOutputStream(file));
                    Toast.makeText(OnlineActivity.this, "PDF fájl legenerálva.", Toast.LENGTH_SHORT).show();
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