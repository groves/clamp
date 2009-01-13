package org.sevorg.clamp;

public class Reflector
{
    public static Object instantiate (Class<?> c)
        throws Exception
    {
        return c.newInstance();
    }

    public static Object call (Object o, String methodName)
        throws Exception
    {
        return o.getClass().getMethod(methodName).invoke(o);
    }

}
