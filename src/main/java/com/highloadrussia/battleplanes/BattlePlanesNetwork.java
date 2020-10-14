package com.highloadrussia.battleplanes;

import com.highloadrussia.battleplanes.entities.MenuAction;
import com.highloadrussia.battleplanes.gui.Gui;
import com.highloadrussia.battleplanes.gui.LanternaGui;
import com.highloadrussia.battleplanes.gui.WrapperWithSocketCommunication;
import com.highloadrussia.battleplanes.services.CommandClient;
import com.highloadrussia.battleplanes.services.CommandServer;
import com.highloadrussia.battleplanes.services.GameService;

import java.io.IOException;

public class BattlePlanesNetwork {

    private final CommandClient client;

    public BattlePlanesNetwork(CommandClient client) {

        this.client = client;
    }

    public static void startGame(CommandClient client) {
        final BattlePlanesNetwork game = new BattlePlanesNetwork(client);
        try {
            game.processGame();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        CommandServer server = new CommandServer(50007);
        server.start();

        while (!server.isClosed()) {
            final CommandClient commandClient = CommandServer.takeClient();
            new Thread(() -> startGame(commandClient)).start();
        }
        // TODO Should I close all clients or wait it?
    }

    public void processGame() throws IOException, InterruptedException {
        Gui gui = new WrapperWithSocketCommunication(new LanternaGui(), client);
        try {
            gui.init();
            gui.drawMenu();

            while (GameService.pullMenuAction(gui) != MenuAction.EXIT) {
                GameService.playGame(gui);
            }
        } finally {
            System.out.println("GUI exit");
            gui.exit();
        }
    }
}
