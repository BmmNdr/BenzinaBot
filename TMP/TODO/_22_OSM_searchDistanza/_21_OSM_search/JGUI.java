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
    private JButton searchButton;
    private JTable table;
    private JPanel lables;

    // creo la lista di risultati in modo che sia accessibile dai due listener
    List<JResult> risultati = null;

    public JGUI() {
        super("Ricerca tramite OSM");
        setLayout(new BorderLayout());

        // creo gli elementi da mettere nel panel
        searchField = new JTextField();
        searchField.setColumns(30);
        searchButton = new JButton("Cerca");
        table = new JTable();
        lables = new JPanel(new GridLayout(4, 1));

        // creo e aggiungo le lables per l'interfaccia master-detail
        JLabel latLabel = new JLabel("Lat: ");
        JLabel lonLabel = new JLabel("Lon: ");
        JLabel typeLabel = new JLabel("Type: ");
        JLabel classLabel = new JLabel("Class: ");

        lables.add(latLabel);
        lables.add(lonLabel);
        lables.add(typeLabel);
        lables.add(classLabel);

        //creo e aggiungo il searchPanel
        JPanel searchPanel = new JPanel(new FlowLayout());
        searchPanel.add(searchField);
        searchPanel.add(searchButton);
        add(searchPanel, BorderLayout.NORTH);
        add(lables, BorderLayout.SOUTH);
        add(new JScrollPane(table), BorderLayout.CENTER);

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

        // quando viene selezionato un item
        table.getSelectionModel().addListSelectionListener(new ListSelectionListener() {
            public void valueChanged(ListSelectionEvent e) {
                int selectedRow = table.getSelectedRow();
                if (selectedRow >= 0) {
                    JResult result = risultati.get(selectedRow);
                    latLabel.setText("Lat: " + result.getLat());
                    lonLabel.setText("Lon: " + result.getLon());
                    typeLabel.setText("Type: " + result.getType());
                    classLabel.setText("Class: " + result.getClasse());
                }
            }
        });

        setSize(720, 720);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
    }
}