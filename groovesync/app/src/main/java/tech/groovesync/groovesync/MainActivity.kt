package tech.groovesync.groovesync

import android.os.Bundle
import android.support.v4.app.FragmentActivity
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.LatLng

import android.content.Intent
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
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

class MainActivity : FragmentActivity(), OnMapReadyCallback {

    private var mMap: GoogleMap? = null

    private val mOkHttpClient = OkHttpClient()
    private var mAccessToken: String? = null
    private var mCall: Call? = null

    private val redirectUri: String = "groovesync://callback"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val mapFragment = supportFragmentManager
            .findFragmentById(R.id.map) as SupportMapFragment?
        mapFragment!!.getMapAsync(this)
    }

    override fun onNewIntent(intent: Intent?) {
        super.onNewIntent(intent)
    }

    override fun onMapReady(googleMap: GoogleMap) {
        mMap = googleMap
        val northAmerica = LatLng(45.7038948, -100.4260382)
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
            .setScopes(arrayOf("user-read-email","user-top-read"))
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
                    setResponse("Finding "+displayName+"\'s bangers")
                } catch (e: JSONException) {
                    setResponse("Failed to parse data: $e")
                }

            }
        })
    }

    private fun setResponse(text: String) {
        runOnUiThread {
            val responseView = findViewById<TextView>(R.id.response_text_view)
            responseView.text = text

            val connectButton = findViewById<Button>(R.id.connect_button)
            connectButton.visibility = View.GONE

            val findingBangersLayout = findViewById<LinearLayout>(R.id.finding_bangers_layout)
            findingBangersLayout.visibility = View.VISIBLE
        }
    }

    private fun cancelCall() {
        if (mCall != null) {
            mCall!!.cancel()
        }
    }

    private fun createMarker(location: LatLng) {
        mMap!!.addMarker(
            MarkerOptions()
                .position(location)
        )
    }

    companion object {
        val CLIENT_ID = "79adc6c2232740df8b8e157b4cf91b71"
        val AUTH_TOKEN_REQUEST_CODE = 0x10
    }

}