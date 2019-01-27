package tech.groovesync.groovesync

import android.app.Activity
import android.content.Context
import android.os.Bundle
import android.support.v4.app.FragmentActivity
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.LatLng

import khttp.get

import android.content.Intent
import android.graphics.Bitmap
import android.graphics.Canvas
import android.os.AsyncTask
import android.support.annotation.ColorInt
import android.support.annotation.DrawableRes
import android.support.v4.content.ContextCompat
import android.support.v4.content.res.ResourcesCompat
import android.support.v4.graphics.drawable.DrawableCompat
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import com.google.android.gms.maps.model.BitmapDescriptor
import com.google.android.gms.maps.model.BitmapDescriptorFactory
import com.google.android.gms.maps.model.MarkerOptions

import com.spotify.sdk.android.authentication.AuthenticationClient
import com.spotify.sdk.android.authentication.AuthenticationRequest
import com.spotify.sdk.android.authentication.AuthenticationResponse

import org.json.JSONException
import org.json.JSONObject

import java.io.IOException

import okhttp3.Call
import okhttp3.Callback
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import java.net.URL

class MainActivity : FragmentActivity(), OnMapReadyCallback {

    private var mMap: GoogleMap? = null

    private val mOkHttpClient = OkHttpClient()
    private var mAccessToken: String = ""
    private var mCall: Call? = null

    private val redirectUri: String = "groovesync://callback"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val mapFragment = supportFragmentManager
            .findFragmentById(R.id.map) as SupportMapFragment?
        mapFragment!!.getMapAsync(this)
    }

    override fun onMapReady(googleMap: GoogleMap) {
        mMap = googleMap
        val northAmerica = LatLng(47.1152462, -101.3094482)
        mMap!!.moveCamera(CameraUpdateFactory.newLatLng(northAmerica))
        mMap!!.setMinZoomPreference(2.5f)

    }

    override fun onDestroy() {
        cancelCall()
        super.onDestroy()
    }

    fun onRequestTokenClicked(view: View) {
        val request = getAuthenticationRequest(AuthenticationResponse.Type.TOKEN)
        AuthenticationClient.openLoginActivity(this, AUTH_TOKEN_REQUEST_CODE, request)
    }

    private fun getAuthenticationRequest(type: AuthenticationResponse.Type): AuthenticationRequest {
        return AuthenticationRequest.Builder(CLIENT_ID, type, redirectUri)
            .setShowDialog(false)
            .setScopes(arrayOf("user-read-email", "user-top-read"))
            .setCampaign("your-campaign-token")
            .build()
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        val response = AuthenticationClient.getResponse(resultCode, data)

        if (AUTH_TOKEN_REQUEST_CODE == requestCode) {
            mAccessToken = response.accessToken
            updateView()
        }
    }

    fun updateView() {
        val request = Request.Builder()
            .url("https://api.spotify.com/v1/me")
            .addHeader("Authorization", "Bearer " + mAccessToken!!)
            .build()

        cancelCall()
        mCall = mOkHttpClient.newCall(request)

        mCall!!.enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                setResponse("Failed to fetch data: $e")
            }

            @Throws(IOException::class)
            override fun onResponse(call: Call, response: Response) {
                try {
                    val jsonObject = JSONObject(response.body()!!.string())
                    Log.d("user jsonObject", jsonObject.toString())
                    val displayName = jsonObject.get("display_name") as String
                    setResponse("Finding " + displayName + "\'s bangers")
                } catch (e: JSONException) {
                    setResponse("Failed to parse data: $e")
                }

            }
        })
    }

    private fun setResponse(text: String) {
        runOnUiThread {
            val findingBangersTextView = findViewById<TextView>(R.id.response_text_view)
            val connectButton = findViewById<Button>(R.id.connect_button)
            val findingBangersLayout = findViewById<LinearLayout>(R.id.finding_bangers_layout)

            connectButton.visibility = View.GONE

            findingBangersTextView.text = text
            findingBangersLayout.visibility = View.VISIBLE

            //wait for stuff from backend
            BackendTask(this, mAccessToken).execute()
        }
    }

    private fun cancelCall() {
        if (mCall != null) {
            mCall!!.cancel()
        }
    }

    private fun createMarker(location: LatLng, matchLevel: Int) { // add parameter for match level (strong/weak)

        var color: Int? = null

        if (matchLevel < 25) {
            color = R.color.weak
        } else if (matchLevel < 50) {
            color = R.color.mediumWeak
        } else if (matchLevel < 75) {
            color = R.color.mediumStrong
        } else {
            color = R.color.strong
        }

        val markerIcon = vectorToBitmap(
            R.drawable.marker,
            ContextCompat.getColor(
                applicationContext,
                color
            )
        )

        mMap!!.addMarker(
            MarkerOptions()
                .position(location)
                .icon(markerIcon)
                .title(matchLevel.toString() + "% Match")
        )

    }

    private fun vectorToBitmap(@DrawableRes id: Int, @ColorInt color: Int): BitmapDescriptor {
        val vectorDrawable = ResourcesCompat.getDrawable(resources, id, null)
        assert(vectorDrawable != null)
        val bitmap = Bitmap.createBitmap(
            vectorDrawable!!.intrinsicWidth,
            vectorDrawable.intrinsicHeight, Bitmap.Config.ARGB_8888
        )
        val canvas = Canvas(bitmap)
        vectorDrawable.setBounds(0, 0, canvas.width, canvas.height)
        DrawableCompat.setTint(vectorDrawable, color)
        vectorDrawable.draw(canvas)
        return BitmapDescriptorFactory.fromBitmap(bitmap)
    }

    companion object {
        val CLIENT_ID = "79adc6c2232740df8b8e157b4cf91b71"
        val AUTH_TOKEN_REQUEST_CODE = 0x10
    }

    class BackendTask(activity: Activity, accessToken: String ) : AsyncTask<Void, Void, Boolean>() {

        private val activity  = activity
        private val accessToken = accessToken


        override fun doInBackground(vararg params: Void?): Boolean {
            val r = khttp.get(url = "ec2-52-203-144-14.compute-1.amazonaws.com/api/recommendations",
                headers = mapOf(accessToken to "user_token"))
        }

        override fun onPostExecute(result: Boolean?) {
            super.onPostExecute(result)
            val findingBangersLayout = activity.findViewById<LinearLayout>(R.id.finding_bangers_layout)
            val mMatchLevelLayout = activity.findViewById<LinearLayout>(R.id.match_level_layout)

            findingBangersLayout.visibility = View.GONE
            mMatchLevelLayout.visibility = View.VISIBLE

            //populate map with markers

        }
    }

}