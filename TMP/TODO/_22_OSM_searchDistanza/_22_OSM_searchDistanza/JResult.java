public class JResult{
    String displayName, lat, lon;

    public JResult(String displayName, String lat, String lon) {
        this.displayName = displayName;
        this.lat = lat;
        this.lon = lon;
    }

    public String getDisplayName() {
        return displayName;
    }

    public String getLat() {
        return lat;
    }

    public String getLon() {
        return lon;
    }
}