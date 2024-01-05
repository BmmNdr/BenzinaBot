public class JResult{
    String displayName, lat, lon, type, classe;

    public JResult(String displayName, String lat, String lon, String type, String classe) {
        this.displayName = displayName;
        this.lat = lat;
        this.lon = lon;
        this.type = type;
        this.classe = classe;
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

    public String getType() {
        return type;
    }

    public String getClasse() {
        return classe;
    }
}