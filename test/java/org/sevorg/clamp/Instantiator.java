package org.sevorg.clamp;

public class Instantiator
{
    public static Object instantiateAndCall (Class<?> c, String methodName)
        throws Exception
    {
        Object instance = c.newInstance();
        return c.getMethod(methodName).invoke(instance);
    }

}
