import javax.swing.*;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import javax.swing.table.DefaultTableModel;
import javax.xml.parsers.ParserConfigurationException;

import org.xml.sax.SAXException;

import java.awt.*;
import java.util.List;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;

public class JGUI extends JFrame {
    private JTextField searchField;
    private JTextField searchField2;
    private JButton searchButton;
    private JButton searchButton2;
    private JTable table;
    private JTable table2;
    private JPanel lables;

    // booleana per distanza
    boolean isBothSelected = false;

    // creo la lista di risultati in modo che sia accessibile dai due listener
    List<JResult> risultati = null;
    List<JResult> risultati2 = null;
    JResult sel1 = null;
    JResult sel2 = null;

    public JGUI() {
        super("Ricerca tramite OSM");
        setLayout(new BorderLayout());

        // panel per le due tabelle e le tabelle
        JPanel tablePanel = new JPanel();
        table = new JTable();
        table2 = new JTable();
        tablePanel.setLayout(new BoxLayout(tablePanel, BoxLayout.Y_AXIS));
        tablePanel.add(new JScrollPane(table));
        tablePanel.add(new JScrollPane(table2));
        // caselle di ricerca e i due pulsanti
        searchField = new JTextField();
        searchField.setColumns(15);
        searchField2 = new JTextField();
        searchField2.setColumns(15);
        searchButton = new JButton("cerca");
        searchButton2 = new JButton("cerca");
        // grid layout per le lables
        lables = new JPanel(new GridLayout(1, 1));

        // creo e aggiungo la lable per la distanza
        JLabel latLabel = new JLabel("Distanza: ");
        lables.add(latLabel);

        // creo e aggiungo il searchPanel
        JPanel searchPanel = new JPanel(new FlowLayout());

        searchPanel.add(searchField);
        searchPanel.add(searchButton);
        searchPanel.add(searchField2);
        searchPanel.add(searchButton2);

        add(searchPanel, BorderLayout.NORTH);
        add(lables, BorderLayout.SOUTH);
        add(tablePanel, BorderLayout.CENTER);

        // quando viene premuto il bottone
        searchButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // eseguo la ricerca e ottengo la lista di risultati
                String searchQuery = searchField.getText();
                try {
                    risultati = JSearch.getSearch(searchQuery);
                } catch (IOException | SAXException | ParserConfigurationException e1) {
                    e1.printStackTrace();
                }

                // popolo la tabella
                DefaultTableModel tableModel = (DefaultTableModel) table.getModel();
                tableModel.setRowCount(0);
                tableModel.setColumnIdentifiers(new Object[] { "Risultati ricerca" });

                for (JResult result : risultati) {
                    tableModel.addRow(new Object[] { result.getDisplayName() });
                }

            }
        });

        // quando viene premuto il bottone di ricerca 2
        searchButton2.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // eseguo la ricerca e ottengo la lista di risultati
                String searchQuery = searchField2.getText();
                try {
                    risultati2 = JSearch.getSearch(searchQuery);
                } catch (IOException | SAXException | ParserConfigurationException e1) {
                    e1.printStackTrace();
                }
                // popolo la tabella
                DefaultTableModel tableModel = (DefaultTableModel) table2.getModel();
                tableModel.setRowCount(0);
                tableModel.setColumnIdentifiers(new Object[] { "Risultati ricerca" });

                for (JResult result : risultati2) {
                    tableModel.addRow(new Object[] { result.getDisplayName() });
                }
            }
        });

        // quando viene selezionato un item
        table.getSelectionModel().addListSelectionListener(new ListSelectionListener() {
            public void valueChanged(ListSelectionEvent e) {
                int selectedRow = table.getSelectedRow();
                if (selectedRow >= 0) {
                    sel1 = risultati.get(selectedRow);
                    isBothSelected = true;
                }
            }
        });

        // quando viene selezionato un item
        table2.getSelectionModel().addListSelectionListener(new ListSelectionListener() {
            public void valueChanged(ListSelectionEvent e) {
                int selectedRow = table.getSelectedRow();
                if (selectedRow >= 0) {
                    sel2 = risultati2.get(selectedRow);
                    if(isBothSelected)
                        latLabel.setText("Distanza: " + distance(Double.parseDouble(sel1.lat), Double.parseDouble(sel2.lat), Double.parseDouble(sel1.lon), Double.parseDouble(sel2.lon)));
                }
            }
        });

        setSize(720, 720);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
    }

    public static double distance(double lat1, double lat2, double lon1, double lon2) {
        final int R = 6371;
        double latDistance = Math.toRadians(lat2 - lat1);
        double lonDistance = Math.toRadians(lon2 - lon1);
        double a = Math.sin(latDistance / 2) * Math.sin(latDistance / 2)
                + Math.cos(Math.toRadians(lat1)) * Math.cos(Math.toRadians(lat2))
                        * Math.sin(lonDistance / 2) * Math.sin(lonDistance / 2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        double distance = R * c;
        return distance;
    }
}