package org.sevorg.clamp;

import org.objectweb.asm.MethodVisitor;
import org.objectweb.asm.Type;



public class AbstractClassBuilder extends InterfaceBuilder
{

    public AbstractClassBuilder (String name)
    {
        super(name);
    }

    /**
     * Makes a constructor that just calls its no-arg super constructor and takes the given args.
     */
    public void addConstructor (Class<?>[] argTypes, Class<?>[] exceptions)
    {
        // TODO - call through to super with the args
        String desc = makeMethodDesc(Void.TYPE, argTypes);
        MethodVisitor mv = cw.visitMethod(ACC_PUBLIC, "<init>", desc, null, makeExcepts(exceptions));
        mv.visitCode();
        mv.visitVarInsn(ALOAD, 0);
        mv.visitMethodInsn(INVOKESPECIAL,
            Type.getInternalName(Object.class),
            "<init>",
            makeMethodDesc(Void.TYPE, new Class[0]));
        mv.visitInsn(RETURN);
        mv.visitMaxs(0, 0);
        mv.visitEnd();
    }

    @Override
    protected int getClassAccess ()
    {
        return ACC_PUBLIC + ACC_ABSTRACT;
    }

}
