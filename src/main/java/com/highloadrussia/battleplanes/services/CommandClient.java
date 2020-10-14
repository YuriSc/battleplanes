package com.highloadrussia.battleplanes.services;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.highloadrussia.battleplanes.entities.Game;
import com.highloadrussia.battleplanes.entities.PlayerAction;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;

public class CommandClient {

    private final Socket client;
    private volatile boolean isClosed = false;
    private final DataOutputStream out;
    private final DataInputStream in;
    private final ObjectMapper mapper = new ObjectMapper();

    public CommandClient(Socket client) throws IOException {
        this.client = client;
        this.out = new DataOutputStream(client.getOutputStream());
        System.out.println("DataOutputStream  created");

        // канал чтения из сокета
        this.in = new DataInputStream(client.getInputStream());
        System.out.println("DataInputStream created");
    }

    public void close() {
        try {
            isClosed = true;
            client.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public PlayerAction getPlayerAction() {
        try {
            if (!isClientConnected()) {
                return PlayerAction.EXIT;
            }
            return PlayerAction.valueOf(in.readUTF());
        } catch (Exception e) {
            return PlayerAction.NONE;
        }
    }

    public void sendGameState(Game game) {
        if (!isClientConnected()) {
            return;
        }
        try {
            out.writeUTF(mapper.writeValueAsString(game));
        } catch (IOException e) {
            e.printStackTrace();
            close();
        }
    }

    public boolean isClientConnected() {
        return !isClosed && client.isConnected();
    }
}
