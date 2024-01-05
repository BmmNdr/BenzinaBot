import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.StringReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.List;

import javax.security.sasl.AuthorizeCallback;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.w3c.dom.NamedNodeMap;

public class JSearch {

    public static List<JResult> getSearch(String searchQuery)
            throws IOException, SAXException, IOException, ParserConfigurationException {
        // prendo il risultato della ricerca
        URL url = new URL("https://nominatim.openstreetmap.org/search?q=" + URLEncoder.encode(searchQuery, "UTF-8")
                + "&format=xml" + "&addressdetails=1");

                System.out.println(url);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));

        // lo metto in una stringa (XML)
        String inputLine;
        StringBuilder response = new StringBuilder();
        while ((inputLine = in.readLine()) != null) {
            response.append(inputLine);
        }
        in.close();
        String xmlString = response.toString();

        // costruisco una NodeList con i risultati
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setNamespaceAware(true);
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document document = builder.parse(new InputSource(new StringReader(xmlString)));
        Node searchResultsNode = document.getFirstChild();
        NodeList nodeList = searchResultsNode.getChildNodes();

        // la converto in una lista di JResult
        List<JResult> risultati = new ArrayList<>();
        for (int i = 0; i < nodeList.getLength(); i++) {
            Node node = nodeList.item(i);
            if (node.getNodeName().equals("place")) {
                NamedNodeMap attributes = node.getAttributes();
                String displayName = attributes.getNamedItem("display_name").getNodeValue();
                String lat = attributes.getNamedItem("lat").getNodeValue();
                String lon = attributes.getNamedItem("lon").getNodeValue();
                String type = attributes.getNamedItem("type").getNodeValue();
                String classe = attributes.getNamedItem("class").getNodeValue();
                JResult tmp = new JResult(displayName, lat, lon, type, classe);
                risultati.add(tmp);
            }
        }

        // ritorno la lista
        return risultati;
    }
}