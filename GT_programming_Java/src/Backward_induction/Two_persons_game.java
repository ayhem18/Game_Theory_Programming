package Backward_induction;

import java.util.*;

class TwoValueGame {
    static final int ONE = 1;
    static final int TEN = 10;

    public static int minList(List<Integer> list) {
        return list.stream()                        // Stream<Integer>
                .mapToInt(v -> v)               // IntStream
                .min()                          // OptionalInt
                .orElse(Integer.MAX_VALUE);
    }
    public static Set<Integer> nextFinalPositions(int minPosition, Set<Integer> currentFinalPas) {
        Set<Integer> possible = new HashSet<>();
        for (int fp : currentFinalPas) {
            possible.add(fp - ONE - ONE);
            possible.add(fp - TEN - TEN);
            possible.add(fp - TEN - ONE);
        }
        // remove any values less than minPosition
        possible.removeIf(x -> x < minPosition);
        // remove any values that are already in the current final positions
        possible.removeIf(currentFinalPas::contains);

        Set<Integer> finalPositions = new HashSet<>();
        for (int fp : possible) {
            if (!currentFinalPas.contains(fp + ONE) && currentFinalPas.contains(fp + ONE + TEN)
                    && currentFinalPas.contains(fp + ONE + ONE)) {
                finalPositions.add(fp);
            }

            if (!currentFinalPas.contains(fp + TEN) && currentFinalPas.contains(fp + TEN + ONE)
                    && currentFinalPas.contains(fp + TEN + TEN)) {
                finalPositions.add(fp);
            }
        }
        return finalPositions;
    }

    public static void solve(int minPosition, Set<Integer> w0) {
        boolean end;
        int i = 1;
        Set<Integer> finalPos = new HashSet<>(w0);
        Set<Integer> newFinal = nextFinalPositions(minPosition, w0);
        System.out.println("W" + i + ": " + finalPos);

        while (true) {
            finalPos.addAll(newFinal);
            end = newFinal.isEmpty();
            if (end) break;
            i++;
            System.out.println("W" + i + ": " + finalPos);
            newFinal = nextFinalPositions(minPosition, finalPos);
        }
    }

    public static void main(String[] args) {
        Set<Integer> w0 = new HashSet<>();
        for (int i = 109; i >= 100; i--) {
            w0.add(i);
        }

        solve(1, w0);
    }
}