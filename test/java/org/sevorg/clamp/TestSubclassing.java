package org.sevorg.clamp;

import java.util.List;

public class TestSubclassing
{

    public static void manipulate (List<Integer> list)
    {
        if (list.get(5) != 5 || list.size() != 10) {
            throw new RuntimeException();
        }
        int idx = 0;
        for (Integer integer : list) {
            if (integer != idx++) {
                throw new RuntimeException();
            }
        }
    }
}
