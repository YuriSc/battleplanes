package com.highloadrussia.battleplanes.services;

import java.io.IOException;
import java.net.ServerSocket;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

public class CommandServer extends Thread {

    private static final BlockingQueue<CommandClient> clients = new LinkedBlockingQueue<>();

    private final ServerSocket server;
    private volatile boolean running = true;

    public CommandServer(int port) {
        try {
            server = new ServerSocket(port, 1);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public void close() {
        running = false;
        try {
            server.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public boolean isClosed() {
        return server.isClosed();
    }

    public static CommandClient takeClient() {
        try {
            return clients.take();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            // Interrupt will throw exception and this code never will be run
            return null;
        }
    }


    @Override
    public void run() {
        while (running) {
            try {
                System.out.println("Waiting client");
                clients.add(new CommandClient(server.accept()));
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
